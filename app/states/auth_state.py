import reflex as rx
import hashlib
import json
import re


class AuthState(rx.State):
    show_login_modal: bool = False
    show_signup_modal: bool = False
    login_email: str = ""
    login_password: str = ""
    login_error: str = ""
    login_loading: bool = False
    show_login_password: bool = False
    signup_name: str = ""
    signup_email: str = ""
    signup_password: str = ""
    signup_confirm_password: str = ""
    signup_error: str = ""
    signup_field_errors: dict[str, str] = {}
    signup_loading: bool = False
    show_signup_password: bool = False
    show_signup_confirm: bool = False
    user_list: list[dict[str, str]] = []
    current_user: dict[str, str] = {}
    show_profile_dropdown: bool = False
    _auth_initialized: bool = False

    @rx.var
    def is_logged_in(self) -> bool:
        return bool(self.current_user.get("email"))

    @rx.var
    def user_initial(self) -> str:
        if self.is_logged_in:
            name = self.current_user.get("name", "?")
            return name[0].upper() if name else "?"
        return "?"

    @rx.var
    def signup_valid(self) -> bool:
        errors = self._validate_signup()
        return len(errors) == 0

    def _validate_signup(self) -> dict[str, str]:
        errors = {}
        if not self.signup_name.strip():
            errors["name"] = "Name is required"
        email_pattern = "^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$"
        if not self.signup_email.strip() or not re.match(
            email_pattern, self.signup_email.strip()
        ):
            errors["email"] = "Valid email is required"
        elif any(
            (
                u.get("email") == self.signup_email.strip().lower()
                for u in self.user_list
            )
        ):
            errors["email"] = "This email is already registered"
        if len(self.signup_password) < 6:
            errors["password"] = "Password must be at least 6 characters"
        if self.signup_password != self.signup_confirm_password:
            errors["confirm_password"] = "Passwords do not match"
        return errors

    def _clear_login_fields(self):
        self.login_email = ""
        self.login_password = ""
        self.login_error = ""
        self.show_login_password = False

    def _clear_signup_fields(self):
        self.signup_name = ""
        self.signup_email = ""
        self.signup_password = ""
        self.signup_confirm_password = ""
        self.signup_error = ""
        self.signup_field_errors = {}
        self.show_signup_password = False
        self.show_signup_confirm = False

    @rx.event
    def open_login_modal(self):
        self.show_login_modal = True
        self.show_signup_modal = False
        self._clear_login_fields()

    @rx.event
    def open_signup_modal(self):
        self.show_signup_modal = True
        self.show_login_modal = False
        self._clear_signup_fields()

    @rx.event
    def close_modals(self):
        self.show_login_modal = False
        self.show_signup_modal = False
        self._clear_login_fields()
        self._clear_signup_fields()

    @rx.event
    def toggle_profile_dropdown(self):
        self.show_profile_dropdown = not self.show_profile_dropdown

    @rx.event
    def close_profile_dropdown(self):
        self.show_profile_dropdown = False

    @rx.event
    def set_login_email(self, value: str):
        self.login_email = value

    @rx.event
    def set_login_password(self, value: str):
        self.login_password = value

    @rx.event
    def toggle_login_password(self):
        self.show_login_password = not self.show_login_password

    @rx.event
    def set_signup_name(self, value: str):
        self.signup_name = value

    @rx.event
    def set_signup_email(self, value: str):
        self.signup_email = value

    @rx.event
    def set_signup_password(self, value: str):
        self.signup_password = value

    @rx.event
    def set_signup_confirm_password(self, value: str):
        self.signup_confirm_password = value

    @rx.event
    def toggle_signup_password(self):
        self.show_signup_password = not self.show_signup_password

    @rx.event
    def toggle_signup_confirm(self):
        self.show_signup_confirm = not self.show_signup_confirm

    @rx.event
    async def handle_signup(self, form_data: dict[str, str]):
        self.signup_name = str(form_data.get("name", ""))
        self.signup_email = str(form_data.get("email", ""))
        self.signup_password = str(form_data.get("password", ""))
        self.signup_confirm_password = str(form_data.get("confirm_password", ""))
        self.signup_field_errors = self._validate_signup()
        if self.signup_field_errors:
            return
        self.signup_loading = True
        yield
        password_hash = hashlib.sha256(self.signup_password.encode()).hexdigest()
        new_user = {
            "name": self.signup_name.strip(),
            "email": self.signup_email.strip().lower(),
            "password_hash": password_hash,
        }
        self.user_list.append(new_user)
        self.current_user = {"name": new_user["name"], "email": new_user["email"]}
        yield rx.call_script(
            f"localStorage.setItem('medismart_users', JSON.stringify({json.dumps(self.user_list)}));"
        )
        yield rx.call_script(
            f"localStorage.setItem('medismart_current_user', JSON.stringify({json.dumps(self.current_user)}));"
        )
        self.signup_loading = False
        self.show_signup_modal = False
        self._clear_signup_fields()
        yield rx.toast(f"Welcome to MediSmart, {new_user['name']}! 🎉", duration=4000)

    @rx.event
    async def handle_login(self, form_data: dict[str, str]):
        self.login_email = str(form_data.get("email", ""))
        self.login_password = str(form_data.get("password", ""))
        self.login_error = ""
        if not self.login_email or not self.login_password:
            self.login_error = "Please fill in all fields"
            return
        self.login_loading = True
        yield
        password_hash = hashlib.sha256(self.login_password.encode()).hexdigest()
        email = self.login_email.strip().lower()
        matched_user = None
        for user in self.user_list:
            if (
                user.get("email") == email
                and user.get("password_hash") == password_hash
            ):
                matched_user = user
                break
        if not matched_user:
            self.login_loading = False
            self.login_error = "Invalid email or password"
            return
        self.current_user = {
            "name": matched_user.get("name", ""),
            "email": matched_user.get("email", ""),
        }
        yield rx.call_script(
            f"localStorage.setItem('medismart_current_user', JSON.stringify({json.dumps(self.current_user)}));"
        )
        self.login_loading = False
        self.show_login_modal = False
        self._clear_login_fields()
        yield rx.toast(
            f"Welcome back, {matched_user.get('name', '')}! 👋", duration=3000
        )

    @rx.event
    def handle_logout(self):
        self.current_user = {}
        self.show_profile_dropdown = False
        yield rx.call_script("localStorage.removeItem('medismart_current_user');")
        yield rx.toast("Logged out successfully", duration=2000)

    @rx.event
    def load_auth_data(self, data: list):
        if not data or not isinstance(data, list) or len(data) < 2:
            self._auth_initialized = True
            return
        users = data[0]
        current = data[1]
        if users and isinstance(users, list):
            self.user_list = users
        if current and isinstance(current, dict) and current.get("email"):
            self.current_user = current
        self._auth_initialized = True

    @rx.event
    def init_auth(self):
        if self._auth_initialized:
            return
        return rx.call_script(
            """
            (function() {
                try {
                    var users = JSON.parse(localStorage.getItem('medismart_users') || '[]');
                    var current = JSON.parse(localStorage.getItem('medismart_current_user') || '{}');
                    return [users, current];
                } catch(e) {
                    return [[], {}];
                }
            })()
            """,
            callback=AuthState.load_auth_data,
        )