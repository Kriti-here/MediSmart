import reflex as rx
from app.states.chat_state import ChatState, ChatMessage


def chat_message(msg: ChatMessage) -> rx.Component:
    return rx.cond(
        msg["role"] == "user",
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    msg["content"], class_name="text-sm font-medium whitespace-pre-wrap"
                ),
                class_name="bg-blue-600 text-white rounded-2xl rounded-tr-sm px-4 py-2 max-w-[85%] shadow-sm",
            ),
            class_name="flex justify-end w-full mb-4",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon(
                    "bot", class_name="h-5 w-5 text-gray-500 mr-2 flex-shrink-0 mt-1"
                ),
                rx.el.div(
                    rx.el.p(
                        msg["content"],
                        class_name="text-sm text-gray-800 font-medium whitespace-pre-wrap",
                    ),
                    class_name="bg-gray-100 rounded-2xl rounded-tl-sm px-4 py-2 max-w-[85%] shadow-sm",
                ),
                class_name="flex items-start w-full mb-4",
            )
        ),
    )


def suggested_question_chip(question: str) -> rx.Component:
    return rx.el.button(
        question,
        on_click=lambda: ChatState.send_suggested_question(question),
        class_name="text-xs text-blue-600 bg-blue-50 hover:bg-blue-100 border border-blue-200 rounded-full px-3 py-1.5 whitespace-nowrap transition-colors flex-shrink-0",
    )


def typing_indicator() -> rx.Component:
    return rx.el.div(
        rx.icon("bot", class_name="h-5 w-5 text-gray-400 mr-2"),
        rx.el.div(
            rx.el.div(
                class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce",
                style={"animationDelay": "0ms"},
            ),
            rx.el.div(
                class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce",
                style={"animationDelay": "150ms"},
            ),
            rx.el.div(
                class_name="w-2 h-2 bg-gray-400 rounded-full animate-bounce",
                style={"animationDelay": "300ms"},
            ),
            class_name="bg-gray-100 rounded-2xl rounded-tl-sm px-4 py-3 flex gap-1 items-center",
        ),
        class_name="flex items-start w-full mb-4",
    )


def quick_symptoms_chips() -> rx.Component:
    symptoms = [
        ("🤕", "Headache"),
        ("🤒", "Fever"),
        ("🔥", "Acidity"),
        ("🤧", "Allergy"),
        ("🦴", "Joint Pain"),
        ("🤒", "Cold"),
    ]
    return rx.cond(
        ChatState.messages.length() <= 2,
        rx.el.div(
            rx.el.p(
                "Quick symptoms:",
                class_name="text-[10px] text-gray-400 font-bold uppercase tracking-wider mb-2 px-3 pt-2",
            ),
            rx.el.div(
                rx.foreach(
                    symptoms,
                    lambda s: rx.el.button(
                        rx.el.span(s[0], class_name="mr-1"),
                        s[1],
                        on_click=lambda: ChatState.send_suggested_question(
                            f"I have {s[1].lower()}"
                        ),
                        class_name="text-xs text-gray-600 bg-white hover:bg-gray-50 border border-gray-200 rounded-full px-3 py-1.5 whitespace-nowrap transition-colors flex-shrink-0 flex items-center shadow-sm",
                    ),
                ),
                class_name="flex flex-wrap gap-1.5 px-3 pb-2",
            ),
            class_name="bg-gray-50 border-t border-gray-100",
        ),
        rx.fragment(),
    )


def chat_widget() -> rx.Component:
    return rx.el.div(
        rx.cond(
            ChatState.is_chat_open,
            rx.el.div(
                rx.el.div(
                    rx.el.div(
                        rx.icon("bot", class_name="h-6 w-6 text-white mr-2"),
                        rx.el.h3(
                            "MediSmart Assistant", class_name="text-white font-bold"
                        ),
                        class_name="flex items-center",
                    ),
                    rx.el.button(
                        rx.icon(
                            "x",
                            class_name="h-5 w-5 text-blue-100 hover:text-white transition-colors",
                        ),
                        on_click=ChatState.toggle_chat,
                    ),
                    class_name="bg-gradient-to-r from-blue-600 to-indigo-600 p-4 flex justify-between items-center",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.foreach(ChatState.messages, chat_message),
                        rx.cond(ChatState.is_typing, typing_indicator()),
                        class_name="flex flex-col",
                    ),
                    id="chat-messages",
                    class_name="p-4 h-80 md:h-96 overflow-y-auto bg-white",
                ),
                quick_symptoms_chips(),
                rx.el.div(
                    rx.foreach(ChatState.suggested_questions, suggested_question_chip),
                    class_name="flex overflow-x-auto gap-2 p-3 bg-gray-50 border-t border-gray-100 scrollbar-hide",
                ),
                rx.el.form(
                    rx.el.div(
                        rx.el.input(
                            placeholder="Ask about generics, savings...",
                            name="message",
                            class_name="flex-1 border-none focus:ring-0 text-sm px-4 py-3 bg-transparent outline-none",
                            default_value=ChatState.current_message,
                            key=ChatState.current_message,
                        ),
                        rx.el.button(
                            rx.icon("send", class_name="h-4 w-4 text-white"),
                            type="submit",
                            class_name="bg-blue-600 hover:bg-blue-700 p-2 rounded-xl transition-colors shadow-sm mr-2",
                        ),
                        class_name="flex items-center bg-white border-t border-gray-100",
                    ),
                    on_submit=ChatState.send_message,
                    reset_on_submit=True,
                ),
                class_name="absolute bottom-20 right-0 md:right-0 w-[calc(100vw-2rem)] md:w-96 bg-white rounded-2xl shadow-2xl border border-gray-200 overflow-hidden flex flex-col z-50 origin-bottom-right animate-in fade-in zoom-in duration-200",
            ),
        ),
        rx.el.button(
            rx.cond(
                ChatState.is_chat_open,
                rx.icon("chevron-down", class_name="h-6 w-6 text-white"),
                rx.el.div(
                    rx.icon("message-circle-question", class_name="h-6 w-6 text-white"),
                    rx.el.span(
                        rx.el.span(
                            class_name="animate-ping absolute inline-flex h-full w-full rounded-full bg-red-400 opacity-75"
                        ),
                        rx.el.span(
                            class_name="relative inline-flex rounded-full h-3 w-3 bg-red-500 border-2 border-white"
                        ),
                        class_name="absolute top-0 right-0 flex h-3 w-3 -mt-1 -mr-1",
                    ),
                    class_name="relative",
                ),
            ),
            on_click=ChatState.toggle_chat,
            class_name="absolute bottom-0 right-0 bg-blue-600 hover:bg-blue-700 p-4 rounded-full shadow-xl hover:shadow-2xl transition-all duration-300 hover:scale-105 z-50 flex items-center justify-center",
        ),
        class_name="fixed bottom-6 right-6 z-50",
    )