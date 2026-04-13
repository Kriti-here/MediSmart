import reflex as rx
from app.states.checkout_state import CheckoutState


def cart_item_row(item: dict) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h4(
                item["name"], class_name="text-sm font-semibold text-gray-900 truncate"
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("minus", class_name="h-3 w-3"),
                    on_click=lambda: CheckoutState.update_qty(
                        item["name"], item["qty"].to(int) - 1
                    ),
                    class_name="bg-gray-100 hover:bg-gray-200 text-gray-600 rounded p-1 transition-colors",
                ),
                rx.el.span(
                    item["qty"].to(str), class_name="text-xs font-bold w-6 text-center"
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-3 w-3"),
                    on_click=lambda: CheckoutState.update_qty(
                        item["name"], item["qty"].to(int) + 1
                    ),
                    class_name="bg-gray-100 hover:bg-gray-200 text-gray-600 rounded p-1 transition-colors",
                ),
                rx.el.span(
                    f"× ₹{item['price']}", class_name="text-xs text-gray-500 ml-2"
                ),
                class_name="flex items-center mt-2",
            ),
            class_name="flex-1 min-w-0 pr-4",
        ),
        rx.el.div(
            rx.el.p(
                f"₹{item['price'].to(float) * item['qty'].to(float)}",
                class_name="text-sm font-bold text-gray-900 whitespace-nowrap mr-3",
            ),
            rx.el.button(
                rx.icon(
                    "trash-2",
                    class_name="h-4 w-4 text-red-400 hover:text-red-600 transition-colors",
                ),
                on_click=lambda: CheckoutState.remove_from_cart(item["name"]),
                class_name="p-1",
            ),
            class_name="flex items-center",
        ),
        class_name="flex justify-between items-center py-4 border-b border-gray-100 last:border-0",
    )


def cart_drawer() -> rx.Component:
    return rx.cond(
        CheckoutState.show_cart_drawer,
        rx.el.div(
            rx.el.div(
                on_click=CheckoutState.close_cart_drawer,
                class_name="fixed inset-0 bg-black/60 backdrop-blur-sm z-[100] animate-in fade-in duration-200",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("shopping-cart", class_name="h-5 w-5 text-gray-900"),
                        rx.el.h2(
                            "Your Cart",
                            class_name="text-xl font-bold text-gray-900 ml-2",
                        ),
                        rx.cond(
                            CheckoutState.cart_item_count > 0,
                            rx.el.span(
                                CheckoutState.cart_item_count,
                                class_name="ml-2 bg-blue-100 text-blue-700 text-xs font-bold px-2 py-0.5 rounded-full",
                            ),
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.button(
                        rx.icon(
                            "x",
                            class_name="h-5 w-5 text-gray-500 hover:text-gray-800 transition-colors",
                        ),
                        on_click=CheckoutState.close_cart_drawer,
                    ),
                    class_name="flex justify-between items-center p-6 border-b border-gray-100 shrink-0",
                ),
                rx.cond(
                    CheckoutState.cart_items.length() > 0,
                    rx.el.div(
                        rx.el.div(
                            rx.foreach(CheckoutState.cart_items, cart_item_row),
                            class_name="p-6 overflow-y-auto flex-1",
                        ),
                        rx.el.div(
                            rx.el.div(
                                rx.el.span("Subtotal", class_name="text-gray-500"),
                                rx.el.span(
                                    f"₹{CheckoutState.cart_total}",
                                    class_name="font-medium text-gray-900",
                                ),
                                class_name="flex justify-between mb-2 text-sm",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Total",
                                    class_name="text-lg font-bold text-gray-900",
                                ),
                                rx.el.span(
                                    f"₹{CheckoutState.cart_total}",
                                    class_name="text-2xl font-black text-blue-600",
                                ),
                                class_name="flex justify-between items-center mb-6",
                            ),
                            rx.el.button(
                                "Proceed to Checkout",
                                on_click=[
                                    CheckoutState.close_cart_drawer,
                                    rx.redirect("/checkout"),
                                ],
                                class_name="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-bold py-4 rounded-xl shadow-lg transition-all",
                            ),
                            rx.el.button(
                                "Continue Shopping",
                                on_click=CheckoutState.close_cart_drawer,
                                class_name="w-full mt-3 text-center text-sm font-semibold text-gray-500 hover:text-gray-800 transition-colors py-2",
                            ),
                            class_name="p-6 border-t border-gray-100 bg-gray-50 shrink-0",
                        ),
                        class_name="flex flex-col h-full overflow-hidden",
                    ),
                    rx.el.div(
                        rx.icon(
                            "shopping-bag",
                            class_name="h-20 w-20 text-gray-200 mx-auto mb-4",
                        ),
                        rx.el.h3(
                            "Your cart is empty",
                            class_name="text-xl font-bold text-gray-900 mb-2",
                        ),
                        rx.el.p(
                            "Browse our shop to find affordable medicines",
                            class_name="text-gray-500 mb-8",
                        ),
                        rx.el.button(
                            "Browse Shop",
                            on_click=[
                                CheckoutState.close_cart_drawer,
                                rx.redirect("/shop"),
                            ],
                            class_name="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-xl font-bold shadow-lg transition-all",
                        ),
                        class_name="flex-1 flex flex-col items-center justify-center p-6 text-center",
                    ),
                ),
                class_name="fixed right-0 top-0 h-full w-full sm:w-96 bg-white shadow-2xl z-[101] flex flex-col animate-in slide-in-from-right duration-300",
            ),
        ),
    )