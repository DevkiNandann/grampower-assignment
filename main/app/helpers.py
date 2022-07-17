from app.models import Meter, Reading

def save_meter_data_in_db(meter_data: dict):
    """
    this function saves the meter data from mqtt in database.

    Args:
        meter_data (dict): meter data
    """
    try:
        if not meter_data:
            return False
        meter_address = meter_data.get("meter_address")
        meter_exists_qs = Meter.objects.filter(meter_address=meter_address)
        if meter_exists_qs.exists():
            meter = meter_exists_qs.first()
        else:
            meter = Meter.objects.create(
                meter_address=meter_address
            )

        Reading.objects.create(
            meter=meter,
            voltage=meter_data.get("voltage"),
            active_power=meter_data.get("active_power_W"),
            apparent_power=meter_data.get("apparent_power_VA"),
            active_energy=meter_data.get("active_energy_Wh"),
            apparent_energy=meter_data.get("apparent_energy_VAh"),
            phase_current=meter_data.get("phase_current"),
            neutral_current=meter_data.get("neutral_current"),
            frequency=meter_data.get("frequency"),
            power_factor=meter_data.get("PF"),
            meter_time=meter_data.get("meter_time")
        )
    except Exception as ex:
        print(ex)
    return True

def get_chart_data(meters_data: list)-> list:
    """
    this helper method creates a data to be passed in chart

    Args:
        meters_data (list): list of meters data for a meter address

    Returns:
        list: chart data
    """
    chart_data = [['Time (HH:MM)', 'Active Power']]
    for data in meters_data:
        response = [data.meter_time.strftime("%H:%m"), data.active_power] 
        chart_data.append(response)

    return chart_data
