from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from tools.validation import (
    SemanticValidator,
    Violation,
    validate_semantics,
)
from tools.validation.semantic_checks import validate_repository_semantics


def _series(
    root: str,
    values: list[str],
    period: str = "2024-01-01T00:00:00Z/PT2H",
    granularity: str = "PT1H",
) -> dict:
    return {
        root: {
            "period": period,
            "granularity": granularity,
            "values": [{"timestamp": value} for value in values],
        }
    }


def _balancing_values(
    values: list[tuple[str, str]],
    quality: str = "preliminary",
) -> list[dict]:
    return [
        {
            "periodStart": period_start,
            "periodEnd": period_end,
            "quantity": 0,
            "quality": quality,
        }
        for period_start, period_end in values
    ]


def _balancing_payload(
    quantity_type: str,
    values: list[tuple[str, str]],
    quality: str = "preliminary",
    sub_type: str = "ContinuousBalancing",
) -> dict:
    return {
        "message": {
            "type": "BALANCING",
            "subType": sub_type,
        },
        "balancingData": {
            "balancingFigures": [
                {
                    "quantityType": quantity_type,
                    "values": _balancing_values(values, quality),
                }
            ]
        },
    }


@pytest.mark.parametrize(
    ("message_type", "sub_type", "payload", "path"),
    [
        (
            "ALLOCATION",
            "Nomination",
            {
                "allocationData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                    "allocations": [
                        {
                            "values": [
                                {
                                    "timestamp": "bad",
                                }
                            ]
                        }
                    ],
                }
            },
            "/allocationData/allocations/0/values/0/timestamp",
        ),
        (
            "ALLOCATION",
            "QuantityDeclaration",
            {
                "allocationData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                    "allocations": [
                        {
                            "values": [
                                {
                                    "timestamp": "bad",
                                }
                            ]
                        }
                    ],
                }
            },
            "/allocationData/allocations/0/values/0/timestamp",
        ),
        (
            "ALLOCATION",
            "Measurement",
            {
                "allocationData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                    "allocations": [
                        {
                            "values": [
                                {
                                    "timestamp": "bad",
                                }
                            ]
                        }
                    ],
                }
            },
            "/allocationData/allocations/0/values/0/timestamp",
        ),
        (
            "MATCHING",
            "Request",
            {
                "matchingData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                    "accountSpecificData": [
                        {
                            "timeSeries": [
                                {
                                    "values": [
                                        {
                                            "timestamp": "bad",
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                }
            },
            "/matchingData/accountSpecificData/0/timeSeries/0/values/0/timestamp",
        ),
        (
            "MEASUREMENT",
            "Final",
            {
                "measurementData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                    "measurements": [
                        {
                            "values": [
                                {
                                    "timestamp": "bad",
                                }
                            ]
                        }
                    ],
                }
            },
            "/measurementData/measurements/0/values/0/timestamp",
        ),
        (
            "NOMINATION",
            "Physical",
            {
                "nominationData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                    "nominations": [
                        {
                            "values": [
                                {
                                    "timestamp": "bad",
                                }
                            ]
                        }
                    ],
                }
            },
            "/nominationData/nominations/0/values/0/timestamp",
        ),
        (
            "NOMINATIONRESPONSE",
            "Physical",
            {
                "nominationResponseData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                    "nominationResponses": [
                        {
                            "timeSeries": [
                                {
                                    "values": [
                                        {
                                            "timestamp": "bad",
                                        }
                                    ]
                                }
                            ]
                        }
                    ],
                }
            },
            "/nominationResponseData/nominationResponses/0/timeSeries/0/values/0/timestamp",
        ),
        (
            "QUANTITYDECLARATION",
            "Default",
            _series(
                "quantityDeclarationData",
                ["bad"],
                "2024-01-01T00:00:00Z/PT1H",
            ),
            "/quantityDeclarationData/values/0/timestamp",
        ),
        (
            "QUANTITYDECLARATIONRESPONSE",
            "Default",
            {
                "quantityDeclarationResponseData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "timeSeries": [
                        {
                            "granularity": "PT1H",
                            "values": [
                                {
                                    "timestamp": "bad",
                                }
                            ],
                        }
                    ],
                }
            },
            "/quantityDeclarationResponseData/timeSeries/0/values/0/timestamp",
        ),
    ],
)
def test_all_time_series_families_report_nested_timestamp_path(
    message_type,
    sub_type,
    payload,
    path,
):
    errors = validate_semantics(payload, message_type, sub_type)

    assert errors[0].path == path
    assert errors[0].message == (
        "Timestamp must be a timezone-aware date-time."
    )


@pytest.mark.parametrize(
    ("period", "count"),
    [
        ("2024-03-31T00:00:00+01:00/P1D", 23),
        ("2024-10-27T00:00:00+02:00/P1D", 25),
    ],
)
def test_calendar_day_grid_handles_berlin_dst(period, count):
    start = datetime.fromisoformat(
        period.split("/")[0]
    ).astimezone(UTC)

    values = [
        {
            "timestamp": (
                start + timedelta(hours=index)
            ).isoformat().replace("+00:00", "Z")
        }
        for index in range(count)
    ]

    payload = {
        "quantityDeclarationData": {
            "period": period,
            "granularity": "PT1H",
            "values": values,
        }
    }

    assert (
        SemanticValidator(
            "QUANTITYDECLARATION",
            "Default",
        ).validate(payload)
        == ()
    )


def test_continuous_balancing_rejects_overlapping_periods():
    payload = _balancing_payload(
        "BGBalance",
        [
            (
                "2024-01-01T00:00:00Z",
                "2024-01-01T01:00:00Z",
            ),
            (
                "2024-01-01T00:30:00Z",
                "2024-01-01T02:00:00Z",
            ),
        ],
    )

    errors = validate_semantics(
        payload,
        "BALANCING",
        "ContinuousBalancing",
    )

    assert (
        errors[0].path
        == "/balancingData/balancingFigures/0/values/1/periodStart"
    )
    assert errors[0].code == "period_overlap"
    assert "overlaps" in errors[0].message


def test_continuous_balancing_rejects_a_gap():
    payload = _balancing_payload(
        "BGBalance",
        [
            (
                "2024-01-01T00:00:00Z",
                "2024-01-01T01:00:00Z",
            ),
            (
                "2024-01-01T01:30:00Z",
                "2024-01-01T02:00:00Z",
            ),
        ],
    )

    errors = validate_semantics(
        payload,
        "BALANCING",
        "ContinuousBalancing",
    )

    assert errors[0].code == "period_gap"
    assert (
        errors[0].path
        == "/balancingData/balancingFigures/0/values/1/periodStart"
    )


@pytest.mark.parametrize(
    "quantity_type",
    [
        "BGBalanceCumulative",
        "BGBalanceCumulativeExternal",
        "OverallNetworkStatus",
    ],
)
def test_cumulative_balancing_types_check_common_start_and_increasing_end(
    quantity_type,
):
    payload = _balancing_payload(
        quantity_type,
        [
            (
                "2024-01-01T00:00:00Z",
                "2024-01-01T02:00:00Z",
            ),
            (
                "2024-01-01T00:30:00Z",
                "2024-01-01T01:00:00Z",
            ),
        ],
    )

    errors = validate_semantics(
        payload,
        "BALANCING",
        "ContinuousBalancing",
    )

    assert {error.path for error in errors} == {
        (
            "/balancingData/balancingFigures/0/values/1/"
            "periodStart"
        ),
        (
            "/balancingData/balancingFigures/0/values/1/"
            "periodEnd"
        ),
    }


def test_balancing_accepts_multiple_quantity_types():
    payload = {
        "message": {
            "type": "BALANCING",
            "subType": "ContinuousBalancing",
        },
        "balancingData": {
            "balancingFigures": [
                {
                    "quantityType": "BGBalance",
                    "values": _balancing_values(
                        [
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T01:00:00Z",
                            ),
                            (
                                "2024-01-01T01:00:00Z",
                                "2024-01-01T02:00:00Z",
                            ),
                        ]
                    ),
                },
                {
                    "quantityType": "BGBalanceCumulative",
                    "values": _balancing_values(
                        [
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T01:00:00Z",
                            ),
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T02:00:00Z",
                            ),
                        ]
                    ),
                },
                {
                    "quantityType": "BGBalanceCumulativeExternal",
                    "values": _balancing_values(
                        [
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T01:00:00Z",
                            ),
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T02:00:00Z",
                            ),
                        ]
                    ),
                },
                {
                    "quantityType": "OverallNetworkStatus",
                    "values": _balancing_values(
                        [
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T01:00:00Z",
                            ),
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T02:00:00Z",
                            ),
                        ]
                    ),
                },
            ],
        },
    }

    assert (
        validate_semantics(
            payload,
            "BALANCING",
            "ContinuousBalancing",
        )
        == ()
    )


def test_difference_quantities_accepts_difference_balance():
    payload = {
        "message": {
            "type": "BALANCING",
            "subType": "DifferenceQuantities",
        },
        "balancingData": {
            "balancingFigures": [
                {
                    "quantityType": "BGBalance",
                    "values": _balancing_values(
                        [
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T01:00:00Z",
                            ),
                            (
                                "2024-01-01T01:00:00Z",
                                "2024-01-01T02:00:00Z",
                            ),
                        ],
                        quality="closed",
                    ),
                },
                {
                    "quantityType": "BGBalance",
                    "values": _balancing_values(
                        [
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T01:00:00Z",
                            ),
                            (
                                "2024-01-01T01:00:00Z",
                                "2024-01-01T02:00:00Z",
                            ),
                        ],
                        quality="final",
                    ),
                },
                {
                    "quantityType": "BGBalanceDifference",
                    "values": _balancing_values(
                        [
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T01:00:00Z",
                            ),
                            (
                                "2024-01-01T01:00:00Z",
                                "2024-01-01T02:00:00Z",
                            ),
                        ],
                        quality="final",
                    ),
                },
            ],
        },
    }

    assert (
        validate_semantics(
            payload,
            "BALANCING",
            "DifferenceQuantities",
        )
        == ()
    )


def test_balancing_unknown_quantity_type_is_rejected():
    payload = {
        "balancingData": {
            "balancingFigures": [
                {
                    "quantityType": "UnknownQuantityType",
                    "values": _balancing_values(
                        [
                            (
                                "2024-01-01T00:00:00Z",
                                "2024-01-01T01:00:00Z",
                            )
                        ]
                    ),
                }
            ],
        },
    }

    errors = validate_semantics(
        payload,
        "BALANCING",
        "ContinuousBalancing",
    )

    assert errors[0].code == "unsupported_balancing_quantity_type"
    assert (
        errors[0].path
        == "/balancingData/balancingFigures/0/quantityType"
    )


def test_nondivisible_period_and_length_mismatch_have_collection_paths():
    nondivisible = _series(
        "quantityDeclarationData",
        [],
        period="2024-01-01T00:00:00Z/PT90M",
        granularity="PT1H",
    )

    wrong_length = _series(
        "quantityDeclarationData",
        ["2024-01-01T00:00:00Z"],
    )

    nondivisible_errors = validate_semantics(
        nondivisible,
        "QUANTITYDECLARATION",
        "Default",
    )

    wrong_length_errors = validate_semantics(
        wrong_length,
        "QUANTITYDECLARATION",
        "Default",
    )

    assert nondivisible_errors[0].path == "/quantityDeclarationData/period"
    assert nondivisible_errors[0].code == "period_not_divisible"

    assert wrong_length_errors[0].path == "/quantityDeclarationData/values"
    assert wrong_length_errors[0].code == "time_series_length"


@pytest.mark.parametrize(
    ("message_type", "sub_type", "payload", "path"),
    [
        (
            "QUANTITYDECLARATION",
            "Default",
            {
                "quantityDeclarationData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                }
            },
            "/quantityDeclarationData/values",
        ),
        (
            "MEASUREMENT",
            "Final",
            {
                "measurementData": {
                    "period": "2024-01-01T00:00:00Z/PT1H",
                    "granularity": "PT1H",
                }
            },
            "/measurementData/measurements",
        ),
        (
            "BALANCING",
            "ContinuousBalancing",
            {
                "balancingData": {},
            },
            "/balancingData/balancingFigures",
        ),
    ],
)
def test_main_configuration_reports_missing_arrays(
    message_type,
    sub_type,
    payload,
    path,
):
    errors = validate_semantics(payload, message_type, sub_type)

    assert errors[0].code == "missing_array"
    assert errors[0].path == path


def test_equivalent_timezone_offsets_match_the_expected_grid():
    payload = _series(
        "quantityDeclarationData",
        [
            "2023-12-31T23:00:00Z",
            "2024-01-01T01:00:00+01:00",
        ],
        period="2024-01-01T00:00:00+01:00/2024-01-01T02:00:00+01:00",
    )

    assert (
        validate_semantics(
            payload,
            "QUANTITYDECLARATION",
            "Default",
        )
        == ()
    )


def test_period_end_must_be_later_than_start():
    payload = _balancing_payload(
        "BGBalance",
        [
            (
                "2024-01-01T01:00:00Z",
                "2024-01-01T00:00:00Z",
            )
        ],
    )

    errors = validate_semantics(
        payload,
        "BALANCING",
        "ContinuousBalancing",
    )

    assert errors[0].code == "non_positive_period"
    assert (
        errors[0].path
        == "/balancingData/balancingFigures/0/values/0/periodEnd"
    )


@pytest.mark.parametrize(
    "sub_type",
    [
        "ContinuousBalancing",
        "DifferenceQuantities",
    ],
)
def test_balancing_message_subtypes_are_supported(sub_type):
    validator = SemanticValidator("BALANCING", sub_type)

    assert validator.message_type == "BALANCING"
    assert validator.message_sub_type == sub_type


def test_unknown_balancing_subtype_fails_during_configuration():
    with pytest.raises(
        ValueError,
        match="Unsupported balancing semantic profile",
    ):
        SemanticValidator("BALANCING", "Unknown")


def test_violation_is_immutable_and_structured():
    violation = Violation("code", "/path", "message")

    with pytest.raises(AttributeError):
        violation.message = "changed"


def test_repository_wrapper_derives_identity_and_formats_filename():
    payload = {
        "message": {
            "type": "BALANCING",
            "subType": "ContinuousBalancing",
        },
        "balancingData": {
            "balancingFigures": [
                {
                    "quantityType": "BGBalance",
                    "values": [
                        {
                            "periodStart": "2024-01-01T01:00:00Z",
                            "periodEnd": "2024-01-01T00:00:00Z",
                            "quantity": 0,
                            "quality": "preliminary",
                        }
                    ],
                }
            ],
        },
    }

    errors = validate_repository_semantics(
        Path("repository"),
        Path("repository/message.json"),
        payload,
    )

    assert errors == [
        (
            "message.json at "
            "/balancingData/balancingFigures/0/values/0/periodEnd: "
            "Period end must be later than period start."
        )
    ]
