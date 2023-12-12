# Food Delivery Bot Documentation

## Overview

The Food Delivery Bot is designed for selling food and serves three user categories:

1. Buyers
2. Chefs
3. Administrators

## Buyer Features

Buyers can perform the following actions:

- Add/remove dishes to/from their cart
- Add/modify their phone number
- View the quantity of their purchases

## Chef Features

Chefs can:

- View current orders
- Confirm completed orders

## Administrator Features

Administrators have a range of capabilities:

- Add/remove product categories
- Add/remove dishes from selected categories
- Modify dish photo/price/description
- Add/remove administrators/chefs
- View bot statistics (user count)
- Download the database
- Add/remove users to/from the blacklist
- Send broadcasts with or without photos
- View current orders pending administrator confirmation

## System Workflow

1. Users add dishes to their cart and submit an order to the administrator. An order can only be submitted if the user's phone number is provided in their profile.

2. Administrators receive notifications about new orders. They review the order details and contact the user. If the user confirms the order, the administrator clicks "Confirm," and the order is sent to the chef. If canceled, the items return to the user's cart.

3. Chefs receive notifications about new orders. They use the `/chef` command to view all current orders and can confirm orders with a single button click.

4. The entire order is recorded in the database, including the completion time, chef information, chef ID, and the user's dish list.

## Language

The bot operates entirely in the Ukrainian language, and no language selection is required from the user.

## Note

Please ensure that administrators include a message to chefs when confirming orders, e.g., "Order must be completed by the end of the working day."

---

This documentation provides an overview of the Food Delivery Bot, its features, and the workflow for users, chefs, and administrators. Refer to the respective sections for detailed information.
