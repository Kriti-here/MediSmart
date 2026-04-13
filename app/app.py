import reflex as rx
import reflex_enterprise as rxe
from app.pages.index_page import index_page
from app.pages.results_page import results_page
from app.pages.upload_page import upload_page
from app.pages.locator_page import locator_page
from app.pages.compare_page import compare_page
from app.pages.medos_page import medos_page
from app.pages.checkout_page import checkout_page
from app.pages.shop_page import shop_page
from app.pages.dashboard_page import dashboard_page

app = rxe.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
        rx.el.link(
            rel="stylesheet",
            href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css",
            integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=",
            cross_origin="",
        ),
    ],
)
app.add_page(index_page, route="/")
app.add_page(results_page, route="/results")
app.add_page(upload_page, route="/upload")
app.add_page(locator_page, route="/locator")
app.add_page(compare_page, route="/compare")
app.add_page(medos_page, route="/medos")
app.add_page(checkout_page, route="/checkout")
app.add_page(shop_page, route="/shop")
app.add_page(dashboard_page, route="/dashboard")