def calculate_energy_financials(devices):
    total_consumption = sum(
        device["new_index"] - device["old_index"]
        for device in devices
    )

    discount_percent = 0
    total_cost = total_consumption * 3000

    if total_consumption >= 50000:
        discount_percent = 3
        total_cost *= 0.97

    return (
        total_consumption,
        discount_percent,
        int(total_cost)
    )