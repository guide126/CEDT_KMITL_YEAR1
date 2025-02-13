class System:
    def __init__(self):
        self.__user_list = []
        self.__menu_list = []
        self.__payment_method = PaymentMethod()
    
    def search_menu(self):
        pass
    
    def login(self):
        pass
    
    def register(self):
        pass

class User:
    def __init__(self, name, tel, password):
        self.__name = name
        self.__tel = tel
        self.__password = password
    
    def logout(self):
        pass
    
    def update_profile(self):
        pass

class Member(User):
    def __init__(self, name, tel, password):
        super().__init__(name, tel, password)
        self.__order_list = []
        self.__address = None
        self.__payment = None
        self.__point = 0
        self.__coupon_list = []
    
    def place_order(self):
        pass
    
    def exchange_point_to_coupon(self):
        pass
    
    def view_order_history(self):
        pass
    
    def update_address(self):
        pass

class Admin(User):
    def __init__(self, name, tel, password, admin_type):
        super().__init__(name, tel, password)
        self.__type = admin_type
    
    def manage_menu(self):
        pass
    
    def view_orders(self):
        pass

class Menu:
    def __init__(self, category, menu_id, name, price, detail):
        self.__category = category
        self.__menu_id = menu_id
        self.__name = name
        self.__price = price
        self.__detail = detail
    
    def get_details(self):
        pass

class Snack(Menu):
    pass

class MenuSet(Menu):
    def __init__(self, category, menu_id, name, price, detail):
        super().__init__(category, menu_id, name, price, detail)
        self.__menu_set_list = []
    
    def add_menu_item(self):
        pass
    
    def remove_menu_item(self):
        pass
    
    def get_total_price(self):
        pass

class Beverage(Menu):
    def __init__(self, category, menu_id, name, price, detail, size):
        super().__init__(category, menu_id, name, price, detail)
        self.__size = size
    
    def set_size(self, size):
        self.__size = size

class Burger(Menu):
    def __init__(self, category, menu_id, name, price, detail, addon):
        super().__init__(category, menu_id, name, price, detail)
        self.__addon = addon
    
    def add_addon(self, addon):
        self.__addon = addon

class Cart:
    def __init__(self):
        self.__item_list = []
    
    def add_item(self):
        pass
    
    def remove_item(self):
        pass
    
    def get_total(self):
        pass

class CartItem:
    def __init__(self, menu, amount):
        self.__menu = menu
        self.__amount = amount

class Order:
    def __init__(self, order_id, member):
        self.__order_id = order_id
        self.__status = "Waiting"
        self.__member = member
        self.__total_price = 0.0
        self.__cart_items = []
        self.__payment = None
    
    def add_item(self):
        pass
    
    def remove_item(self):
        pass
    
    def calculate_total(self):
        pass
    
    def checkout(self):
        pass

class Address:
    def __init__(self, name, detail):
        self.__name = name
        self.__detail = detail
    
    def update_address(self):
        pass

class PaymentSystem:
    def __init__(self):
        self.__payments = []
    
    def start_payment(self, order, payment_method):
        payment = Payment(
            payment_id=len(self.__payments) + 1,
            date=None,  
            total_price=order.calculate_total(),
            status="Pending",
            discount=0,
            payment_method=payment_method
        )
        
        result = payment_method.process_payment(payment)
        
        if result:
            payment.complete_payment()
            self.__payments.append(payment)
            return {"status": "success", "payment": payment}
        return {"status": "failed"}
    
    def cancel_payment(self, payment):
        if payment.cancel_payment():
            return {"status": "canceled"}
        return {"status": "cannot_cancel"}

    def get_payment_history(self):
        history = []
        for payment in self.__payments:
            history.append({
                "payment_id": payment.payment_id,
                "date": payment.date,
                "total_price": payment.total_price,
                "status": payment.status,
                "payment_method": type(payment.payment_method).__name__
            })
        return history

class Payment:
    def __init__(self, payment_id, date, total_price, status, discount, payment_method):
        self.__payment_id = payment_id
        self.__date = date
        self.__total_price = total_price
        self.__status = status
        self.__discount = discount
        self.__payment_method = payment_method
    
    def cancel_payment(self):
        if self.__status == "Pending":
            self.__status = "Canceled"
            return True
        return False
    
    def complete_payment(self):
        from datetime import datetime
        self.__date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")  # Format as d/m/y and h:m:ss
        self.__status = "Completed"


    @property
    def payment_id(self):
        return self.__payment_id

    @property
    def date(self):
        return self.__date

    @property
    def total_price(self):
        return self.__total_price

    @property
    def status(self):
        return self.__status

    @property
    def payment_method(self):
        return self.__payment_method
class PaymentMethod:
    def __init__(self, payment_method_id=None, payment_method_name=None):
        self.__payment_method_id = payment_method_id
        self.__payment_method_name = payment_method_name
    
    def process_payment(self, payment):
        pass

class QRCode(PaymentMethod):
    def __init__(self, qr_code_data):
        super().__init__()
        self.__qr_code_data = qr_code_data
    
    def process_payment(self, payment):
        try:
            if self.__qr_code_data:
                return True
            return False
        except Exception:
            return False

class CreditCard(PaymentMethod):
    def __init__(self, card_number, expiry_date, cvv):
        super().__init__()
        self.__card_number = card_number
        self.__expiry_date = expiry_date
        self.__cvv = cvv
    
    def process_payment(self, payment):
        try:
            if (self.__card_number and 
                self.__expiry_date and 
                self.__cvv):
                return True
            return False
        except Exception:
            return False

class Coupon:
    def __init__(self, code, discount, expire_date):
        self.__code = code
        self.__discount = discount
        self.__expire_date = expire_date

class MockOrder:
    def __init__(self, total_price):
        self.__total_price = total_price
    
    def calculate_total(self):
        return self.__total_price

# Test Cases

def test_payment_system():
    print("=== เริ่มการทดสอบระบบชำระเงิน ===")
    
    payment_system = PaymentSystem()
    mock_order = MockOrder(1000.0)
    print("\n1. ทดสอบชำระเงินผ่าน QR Code สำเร็จ:")
    qr_payment = QRCode("VALID_QR_CODE")
    result = payment_system.start_payment(mock_order, qr_payment)
    print(f"ผลลัพธ์: {result['status']}")
    print(f"สถานะการชำระเงิน: {result['payment'].status if result['status'] == 'success' else 'N/A'}")
    print("\n1. ทดสอบชำระเงินผ่าน QR Code สำเร็จ:")
    qr_payment = QRCode("VALID_QR_CODE")
    result = payment_system.start_payment(mock_order, qr_payment)
    print(f"ผลลัพธ์: {result['status']}")
    print(f"สถานะการชำระเงิน: {result['payment'].status if result['status'] == 'success' else 'N/A'}")
    print("\n1. ทดสอบชำระเงินผ่าน QR Code สำเร็จ:")
    qr_payment = QRCode("VALID_QR_CODE")
    result = payment_system.start_payment(mock_order, qr_payment)
    print(f"ผลลัพธ์: {result['status']}")
    print(f"สถานะการชำระเงิน: {result['payment'].status if result['status'] == 'success' else 'N/A'}")
    print("\n1. ทดสอบชำระเงินผ่าน QR Code สำเร็จ:")
    qr_payment = QRCode("VALID_QR_CODE")
    result = payment_system.start_payment(mock_order, qr_payment)
    print(f"ผลลัพธ์: {result['status']}")
    print(f"สถานะการชำระเงิน: {result['payment'].status if result['status'] == 'success' else 'N/A'}")
    print("\n1. ทดสอบชำระเงินผ่าน QR Code สำเร็จ:")
    qr_payment = QRCode("VALID_QR_CODE")
    result = payment_system.start_payment(mock_order, qr_payment)
    print(f"ผลลัพธ์: {result['status']}")
    print(f"สถานะการชำระเงิน: {result['payment'].status if result['status'] == 'success' else 'N/A'}")
    print("\n1. ทดสอบชำระเงินผ่าน QR Code สำเร็จ:")
    qr_payment = QRCode("VALID_QR_CODE")
    result = payment_system.start_payment(mock_order, qr_payment)
    print(f"ผลลัพธ์: {result['status']}")
    print(f"สถานะการชำระเงิน: {result['payment'].status if result['status'] == 'success' else 'N/A'}")
    
    # Test 1: Successful QR Code Payment
    print("\n1. ทดสอบชำระเงินผ่าน QR Code สำเร็จ:")
    qr_payment = QRCode("VALID_QR_CODE")
    result = payment_system.start_payment(mock_order, qr_payment)
    print(f"ผลลัพธ์: {result['status']}")
    print(f"สถานะการชำระเงิน: {result['payment'].status if result['status'] == 'success' else 'N/A'}")
    
    # Test 2: Failed QR Code Payment
    print("\n2. ทดสอบชำระเงินผ่าน QR Code ไม่สำเร็จ:")
    invalid_qr = QRCode("")
    result = payment_system.start_payment(mock_order, invalid_qr)
    print(f"ผลลัพธ์: {result['status']}")
    
    # Test 3: Successful Credit Card Payment
    print("\n3. ทดสอบชำระเงินผ่านบัตรเครดิตสำเร็จ:")
    credit_card = CreditCard("4111111111111111", "12/25", "123")
    result = payment_system.start_payment(mock_order, credit_card)
    print(f"ผลลัพธ์: {result['status']}")
    print(f"สถานะการชำระเงิน: {result['payment'].status if result['status'] == 'success' else 'N/A'}")
    
    # Test 4: Attempt to Cancel a Completed Payment
    print("\n4. ทดสอบยกเลิกการชำระเงินที่สำเร็จแล้ว:")
    if result['status'] == 'success':
        cancel_result = payment_system.cancel_payment(result['payment'])
        print(f"ผลลัพธ์การยกเลิก: {cancel_result['status']}")
    else:
        print("ไม่สามารถทดสอบได้: การชำระเงินไม่สำเร็จ")
    
    # Test 5: Cancel a Pending Payment
    print("\n5. ทดสอบยกเลิกการชำระเงินที่รอดำเนินการ:")
    pending_payment = Payment(1002, None, mock_order.calculate_total(), "Pending", 0, qr_payment)
    cancel_result = payment_system.cancel_payment(pending_payment)
    print(f"ผลลัพธ์การยกเลิก: {cancel_result['status']}")
    
    # Test 6: Start Payment with Insufficient Data
    print("\n6. ทดสอบชำระเงินด้วยข้อมูลที่ไม่สมบูรณ์:")
    incomplete_credit_card = CreditCard("", "", "")  # Missing all details
    result = payment_system.start_payment(mock_order, incomplete_credit_card)
    print(f"ผลลัพธ์: {result['status']}")
    
    
    # Test 7
    print("\n7. ประวัติการชำระเงิน:")
    history = payment_system.get_payment_history()
    for record in history:
        print(record)
    print("\n=== การทดสอบเสร็จสิ้น ===")
# Run Tests
if __name__ == "__main__":
    test_payment_system()
