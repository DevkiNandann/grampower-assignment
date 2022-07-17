from django.views import generic
from app.forms import LoginForm
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from app.models import Meter, Reading
from datetime import datetime, timedelta
from app.helpers import get_chart_data

LOGIN_PAGE_TEMPLATE = "login.html"
METER_DETAIL_PAGE_TEMPLATE = "meter_detail.html"
METER_LISTING_PAGE_TEMPLATE = "meter_list.html"


class Login(generic.View):
    login_form = LoginForm()

    def get(self, request):
        """
        this method opens login page

        """
        try:
            return render(
                request,
                LOGIN_PAGE_TEMPLATE,
                {"form": self.login_form},
            )
        except Exception:
            return render(
                request,
                LOGIN_PAGE_TEMPLATE,
                {"form": self.login_form},
            )

    def post(self, request):
        """
        This method is used to validate the login

        Args:
            email: we get this from request, it is the email of admin user trying to make login
            password: we get this from request, it is the password of admin user trying to make login

        """
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")

            user = User.objects.filter(email=email)
            if not user.exists():
                return render(
                    request,
                    LOGIN_PAGE_TEMPLATE,
                    {"form": self.login_form},
                )

            user = user.first()
            is_password_correct = check_password(password, user.password)

            if is_password_correct and user.is_superuser:
                request.session["username"] = user.username
                request.session["admin_name"] = user.username
                request.session["admin_email"] = email
                request.session["is_authenticated"] = True
                return redirect("meter-list")
            else:
                return render(
                    request,
                    LOGIN_PAGE_TEMPLATE,
                    {"form": self.login_form},
                )


class MeterView(generic.View):
    def get(self, request, id=None):
        """
        this method will return meter details if id is provided else listing

        Args:
            id (int, optional): meter id. Defaults to None.
        """
        now = datetime.now() + timedelta(hours=5, minutes=30)
        if id:
            meter_qs = Meter.objects.filter(id=id)
            if not meter_qs.exists():
                return redirect("meter-list")

            meter = meter_qs.first()
            same_address_meter = Reading.objects.filter(meter=meter)

            # first reading of the day
            first_reading = same_address_meter.order_by("meter_time").first()
            first_active_energy = first_reading.active_energy if first_reading else 0

            # recent reading for the day
            recent_reading = same_address_meter.order_by("-meter_time").first()
            recent_active_energy = recent_reading.active_energy  if recent_reading else 0
            total_consumption = recent_active_energy - first_active_energy

            all_readings = same_address_meter.all()

            average_phase_current = sum(reading.phase_current for reading in all_readings)/ len(all_readings)
            average_neutral_current = sum(reading.neutral_current for reading in all_readings)/ len(all_readings)
            average_voltage = sum(reading.voltage for reading in all_readings)/ len(all_readings)

            if now - recent_reading.meter_time > timedelta(hours=1):
                status = "Down"
            else:
                status = "Live"

            response = {
                "id": recent_reading.meter.id,
                "meter_address": recent_reading.meter.meter_address,
                "status": status,
                "meter_time": recent_reading.meter_time.strftime("%d %B %Y %H:%M:%S"),
                "average_voltage": average_voltage,
                "average_neutral_current": average_neutral_current,
                "average_phase_current": average_phase_current,
                "total_consumption": total_consumption,
                "chart_data": get_chart_data(all_readings)
                
            }
            return render(request, METER_DETAIL_PAGE_TEMPLATE, {"data": response})

        meters = Meter.objects.order_by("-id").all()
        data = []
        for meter in meters:
            # atleast one meter will always be present
            reading = Reading.objects.filter(meter=meter).order_by("-meter_time").first()
            meter_data = {
                "id": meter.id,
                "address": meter.meter_address
            }
            if now - reading.meter_time > timedelta(hours=1):
                meter_data["status"] = "Down"
            else:
                meter_data["status"] = "Live"
            data.append(meter_data)

        return render(request, METER_LISTING_PAGE_TEMPLATE, {"data": data})
