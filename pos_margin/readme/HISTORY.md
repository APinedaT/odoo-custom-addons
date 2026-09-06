## 19.0.1.0.0

- Migrate to V19.0
- The frontend margin is now rendered in the totals block of the
  `OrderDisplay` component (the `OrderWidget` component no longer exists).
  As a side effect, the margin of an order is also displayed when reviewing a
  past order from the ticket screen.
- Frontend methods are renamed to the V19.0 camelCase convention:
  `get_margin()` / `get_margin_rate()` / `get_margin_rate_str()` /
  `get_purchase_price()` / `get_iface_display_margin()` become `getMargin()` /
  `getMarginRate()` / `getMarginRateStr()` / `getPurchasePrice()` /
  `getIfaceDisplayMargin()`.
- Fix the `margin_rate` field of the `report.pos.order` report, that was empty
  for every line whose `total_cost` was not computed yet, instead of falling
  back to a null cost like the standard `margin` field does.

## 16.0.1.0.0

- Migrate to V16.0
- Remove the addition of the margin field to `pos.order` and `pos.order.line` introduced in v14.0, 
  as this functionality is already provided by Odoo in v16.0.
- Remove tests.
- Create a `res.config.settings` field pos_iface_display_margin to
  display margins in PoS frontend.

## 14.0.1.0.0

- Migrate to V14.0

## 13.0.1.0.0

- Migrate to V13.0
- Reuse `sale_margin` computation to handle multi currency context.
- Correct computation of margin, if a module that adds `uom_id` on
  `pos.order.line` is installed.
- Add test
