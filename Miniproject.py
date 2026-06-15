import logging

logging.basicConfig(
    filename="energy_monitor.log",
    level=logging.INFO,
    format="[%(asctime)s] [%(levelname)s] %(message)s"
)


class DeviceNotFoundError(Exception):
    pass


class AlreadyOverloadError(Exception):
    pass


def show_devices(devices):
    if not devices:
        print("\nHỆ THỐNG CHƯA CÓ THIẾT BỊ NÀO.")
        return

    print("\n===== DANH SÁCH THIẾT BỊ =====")
    print(
        f"{'ID':<8}"
        f"{'LOCATION':<25}"
        f"{'OLD INDEX':<15}"
        f"{'NEW INDEX':<15}"
        f"{'STATUS':<15}"
    )

    for device in devices:
        print(
            f"{device['id']:<8}"
            f"{device['location']:<25}"
            f"{device['old_index']:<15}"
            f"{device['new_index']:<15}"
            f"{device['status']:<15}"
        )


def find_device(devices, device_id):
    for device in devices:
        if device["id"] == device_id:
            return device
    return None


def get_non_negative_number(message):
    while True:
        try:
            value = int(input(message))

            if value < 0:
                print("Giá trị phải lớn hơn hoặc bằng 0.")
                continue

            return value

        except ValueError:
            print("Vui lòng nhập số hợp lệ.")


def update_indices(devices):
    device_id = input("Nhập mã thiết bị: ").strip()

    device = find_device(devices, device_id)

    if device is None:
        raise DeviceNotFoundError(
            "ERR-E01: Không tìm thấy mã thiết bị."
        )

    old_index = get_non_negative_number(
        "Nhập chỉ số cũ: "
    )

    while True:
        new_index = get_non_negative_number(
            "Nhập chỉ số mới: "
        )

        if new_index < old_index:
            print(
                "ERR-E02: Chỉ số mới không được nhỏ hơn chỉ số cũ."
            )
            continue

        break

    device["old_index"] = old_index
    device["new_index"] = new_index

    logging.info(
        f"Cập nhật chỉ số thành công cho thiết bị {device_id}"
    )


def activate_overload(devices):
    device_id = input(
        "Nhập mã thiết bị cần kiểm tra: "
    ).strip()

    device = find_device(devices, device_id)

    if device is None:
        raise DeviceNotFoundError(
            "ERR-E01: Không tìm thấy mã thiết bị."
        )

    if device["status"] == "Overload":
        raise AlreadyOverloadError(
            "ERR-E04: Thiết bị đã ở trạng thái Overload."
        )

    consumption = (
        device["new_index"] - device["old_index"]
    )

    if consumption > 5000:
        device["status"] = "Overload"

        logging.warning(
            f"Thiết bị {device_id} vượt ngưỡng tiêu thụ an toàn."
        )

        print("Kích hoạt trạng thái Overload thành công.")
    else:
        print("Thiết bị chưa vượt ngưỡng 5000 kWh.")


def calculate_energy_financials(devices):
    total_consumption = sum(
        device["new_index"] - device["old_index"]
        for device in devices
    )

    total_cost = total_consumption * 3000
    discount_percent = 0

    if total_consumption >= 50000:
        discount_percent = 3
        total_cost *= 0.97

    return (
        total_consumption,
        discount_percent,
        int(total_cost)
    )


def display_menu():
    print("\n===== SMART ENERGY MONITOR =====")
    print("1. Xem danh sách thiết bị")
    print("2. Cập nhật chỉ số điện tiêu thụ")
    print("3. Kích hoạt cảnh báo quá tải")
    print("4. Tính tổng điện & chi phí")
    print("5. Thoát")
    print("================================")


def main():
    devices = [
        {
            "id": "M01",
            "location": "Mechanical Shop A",
            "old_index": 1200,
            "new_index": 4500,
            "status": "Normal"
        },
        {
            "id": "M02",
            "location": "Assembly Line B",
            "old_index": 2300,
            "new_index": 8500,
            "status": "Overload"
        }
    ]

    while True:
        display_menu()

        try:
            choice = int(
                input("Chọn chức năng: ")
            )

            if choice == 1:
                show_devices(devices)

            elif choice == 2:
                try:
                    update_indices(devices)
                    print(
                        "Cập nhật chỉ số thành công."
                    )

                except DeviceNotFoundError as error:
                    print(error)

            elif choice == 3:
                try:
                    activate_overload(devices)

                except (
                    DeviceNotFoundError,
                    AlreadyOverloadError
                ) as error:
                    print(error)

            elif choice == 4:
                total_kwh, discount, total_cost = (
                    calculate_energy_financials(
                        devices
                    )
                )

                print(
                    "\n===== BÁO CÁO NĂNG LƯỢNG ====="
                )
                print(
                    f"Tổng điện tiêu thụ: {total_kwh:,} kWh"
                )
                print(
                    f"Chiết khấu áp dụng: {discount}%"
                )
                print(
                    f"Tổng chi phí: {total_cost:,} VND"
                )

            elif choice == 5:
                print(
                    "\nCảm ơn đã sử dụng Smart Energy Monitor!"
                )
                break

            else:
                print(
                    "Lựa chọn không hợp lệ."
                )

        except ValueError:
            print(
                "Vui lòng nhập số từ 1 đến 5."
            )


if __name__ == "__main__":
    main()
