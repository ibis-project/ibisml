from __future__ import annotations

from typing import Any, Iterable, Sequence, Literal

import ibis.expr.types as ir

from ibisml.core import Metadata, Step
from ibisml.select import SelectionType, selector


class ExpandDateTime(Step):
    """A step for expanding date and time columns into one or more features.

    New features will be named ``{input_column}_{component}``. For example, if
    expanding a ``"year"`` component from column ``"x"``, the feature column
    would be named ``"x_year"``.

    Parameters
    ----------
    inputs
        A selection of date and time columns to expand into new features.
    date_components
        A sequence of date components to expand. Options include

        - ``day``: the day of the month as a numeric value
        - ``week``: the week of the year as a numeric value
        - ``month``: the month of the year as a categorical value
        - ``year``: the year as a numeric value
        - ``dow``: the day of the week as a categorical value
        - ``doy``: the day of the year as a numeric value

        Defaults to ``["dow", "month", "year"]``.
    time_components
        A sequence of time components to expand. Options include ``hour``,
        ``minute``, ``second``, and ``millisecond``.

        Defaults to ``["hour", "minute", "second"]``.

    Examples
    --------
    >>> import ibisml as ml

    Expand date and time columns using the default components

    >>> step = ml.ExpandDateTime(ml.datetime())

    Expand specific columns using specific components for date and time

    >>> step = ml.ExpandDateTime(["x", "y"], ["day", "year"], ["hour", "minute"])
    """

    def __init__(
        self,
        inputs: SelectionType,
        datetime_components: list[
            Literal[
                "day",
                "week",
                "month",
                "year",
                "dow",
                "doy",
                "hour",
                "minute",
                "second",
                "millisecond",
            ]
        ] = (
            "day",
            "week",
            "month",
            "year",
            "dow",
            "doy",
            "hour",
            "minute",
        ),
    ):
        self.inputs = selector(inputs)
        self.datetime_components = list(datetime_components)

    def _repr(self) -> Iterable[tuple[str, Any]]:
        yield ("", self.inputs)
        yield ("datetime_components", self.datetime_components)

    def fit_table(self, table: ir.Table, metadata: Metadata) -> None:
        columns = self.inputs.select_columns(table, metadata)

        if "month" in self.datetime_components:
            for col in columns:
                metadata.set_categories(
                    f"{col}_month",
                    [
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                    ],
                )
        if "dow" in self.datetime_components:
            for col in columns:
                metadata.set_categories(
                    f"{col}_dow",
                    [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thurday",
                        "Friday",
                        "Saturday",
                        "Sunday",
                    ],
                )

        self.columns_ = columns

    def transform_table(self, table: ir.Table) -> ir.Table:
        new_cols = []

        for name in self.columns_:
            col = table[name]
            for comp in self.datetime_components:
                if comp == "day":
                    feat = col.day()
                elif comp == "week":
                    feat = col.week_of_year()
                elif comp == "month":
                    feat = col.month() - 1
                elif comp == "year":
                    feat = col.year()
                elif comp == "dow":
                    feat = col.day_of_week.index()
                elif comp == "doy":
                    feat = col.day_of_year()
                elif comp == "hour":
                    feat = col.hour()
                elif comp == "minute":
                    feat = col.minute()
                elif comp == "second":
                    feat = col.second()
                elif comp == "millisecond":
                    feat = col.millisecond()
                new_cols.append(feat.name(f"{name}_{comp}"))

        return table.mutate(new_cols)


class ExpandDate(Step):
    """A step for expanding date columns into one or more features.

    New features will be named ``{input_column}_{component}``. For example, if
    expanding a ``"year"`` component from column ``"x"``, the feature column
    would be named ``"x_year"``.

    Parameters
    ----------
    inputs
        A selection of date columns to expand into new features.
    components
        A sequence of components to expand. Options include

        - ``day``: the day of the month as a numeric value
        - ``week``: the week of the year as a numeric value
        - ``month``: the month of the year as a categorical value
        - ``year``: the year as a numeric value
        - ``dow``: the day of the week as a categorical value
        - ``doy``: the day of the year as a numeric value

        Defaults to ``["dow", "month", "year"]``.

    Examples
    --------
    >>> import ibisml as ml

    Expand date columns using the default components

    >>> step = ml.ExpandDate(ml.date())

    Expand specific columns using specific components

    >>> step = ml.ExpandDate(["x", "y"], ["day", "year"])
    """

    def __init__(
        self,
        inputs: SelectionType,
        components: Sequence[Literal["day", "week", "month", "year", "dow", "doy"]] = (
            "dow",
            "month",
            "year",
        ),
    ):
        self.inputs = selector(inputs)
        self.components = list(components)

    def _repr(self) -> Iterable[tuple[str, Any]]:
        yield ("", self.inputs)
        yield ("components", self.components)

    def fit_table(self, table: ir.Table, metadata: Metadata) -> None:
        columns = self.inputs.select_columns(table, metadata)
        if "month" in self.components:
            for col in columns:
                metadata.set_categories(
                    f"{col}_month",
                    [
                        "January",
                        "February",
                        "March",
                        "April",
                        "May",
                        "June",
                        "July",
                        "August",
                        "September",
                        "October",
                        "November",
                        "December",
                    ],
                )
        if "dow" in self.components:
            for col in columns:
                metadata.set_categories(
                    f"{col}_dow",
                    [
                        "Monday",
                        "Tuesday",
                        "Wednesday",
                        "Thurday",
                        "Friday",
                        "Saturday",
                        "Sunday",
                    ],
                )
        self.columns_ = columns

    def transform_table(self, table: ir.Table) -> ir.Table:
        new_cols = []
        for name in self.columns_:
            col = table[name]
            for comp in self.components:
                if comp == "day":
                    feat = col.day()
                elif comp == "week":
                    feat = col.week_of_year()
                elif comp == "month":
                    feat = col.month() - 1
                elif comp == "year":
                    feat = col.year()
                elif comp == "dow":
                    feat = col.day_of_week.index()
                elif comp == "doy":
                    feat = col.day_of_year()
                new_cols.append(feat.name(f"{name}_{comp}"))
        return table.mutate(new_cols)


class ExpandTime(Step):
    """A step for expanding time columns into one or more features.

    New features will be named ``{input_column}_{component}``. For example, if
    expanding an ``"hour"`` component from column ``"x"``, the feature column
    would be named ``"x_hour"``.

    Parameters
    ----------
    inputs
        A selection of time columns to expand into new features.
    components
        A sequence of components to expand. Options include ``hour``,
        ``minute``, ``second``, and ``millisecond``.

        Defaults to ``["hour", "minute", "second"]``.

    Examples
    --------
    >>> import ibisml as ml

    Expand time columns using the default components

    >>> step = ml.ExpandTime(ml.time())

    Expand specific columns using specific components

    >>> step = ml.ExpandTime(["x", "y"], ["hour", "minute"])
    """

    def __init__(
        self,
        inputs: SelectionType,
        components: Sequence[Literal["hour", "minute", "second", "millisecond"]] = (
            "hour",
            "minute",
            "second",
        ),
    ):
        self.inputs = selector(inputs)
        self.components = list(components)

    def _repr(self) -> Iterable[tuple[str, Any]]:
        yield ("", self.inputs)
        yield ("components", self.components)

    def fit_table(self, table: ir.Table, metadata: Metadata) -> None:
        self.columns_ = self.inputs.select_columns(table, metadata)

    def transform_table(self, table: ir.Table) -> ir.Table:
        new_cols = []
        for name in self.columns_:
            col = table[name]
            for comp in self.components:
                if comp == "hour":
                    feat = col.hour()
                elif comp == "minute":
                    feat = col.minute()
                elif comp == "second":
                    feat = col.second()
                elif comp == "millisecond":
                    feat = col.millisecond()
                new_cols.append(feat.name(f"{name}_{comp}"))
        return table.mutate(new_cols)
