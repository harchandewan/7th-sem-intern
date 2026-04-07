from datetime import datetime, timedelta 
import random


class User:
    def __init__(self, user_id, name, email):
        self.id = user_id
        self.name = name
        self.email = email


class Plan:
    def __init__(self, name, price):
        self.name = name
        self.price = price


class Subscription:
    def __init__(self, user, plan, start_date):
        self.user = user
        self.plan = plan
        self.start_date = start_date
        self.next_billing_date = start_date + timedelta(days=30)
        self.status = "Active"
        self.coupon = None


class Coupon:
    def __init__(self, code, ctype, value):
        self.code = code
        self.type = ctype
        self.value = value


# ---------------------------
# Services
# ---------------------------

class PaymentService:
    def process_payment(self, amount):
        success = random.choice([True, False])
        return success


class BillingService:
    def __init__(self):
        self.payment_service = PaymentService()

    def apply_coupon(self, amount, coupon):
        if not coupon:
            return amount

        if coupon.type == "percent":
            amount -= (amount * coupon.value / 100)
        else:
            amount -= coupon.value

        return max(0, amount)

    def process_payment_with_retry(self, amount, subscription):
        retries = 0

        while retries < 3:
            success = self.payment_service.process_payment(amount)

            if success:
                print(f"[Payment SUCCESS] Amount: ${amount}")
                return True
            else:
                retries += 1
                print(f"[Payment FAILED] Retry {retries}")

        subscription.status = "Overdue"
        print("[Subscription OVERDUE]")
        return False

    def generate_invoice(self, subscription, current_date):
        if subscription.plan.price == 0:
            print("[Free Plan] No billing required.")
            return

        amount = subscription.plan.price
        amount = self.apply_coupon(amount, subscription.coupon)

        print(f"[Invoice Generated] Amount: ${round(amount,2)}")

        self.process_payment_with_retry(amount, subscription)


class SubscriptionService:
    def __init__(self):
        self.subscription = None
        self.billing_service = BillingService()

    def subscribe(self, user, plan):
        current_date = datetime.now()
        self.subscription = Subscription(user, plan, current_date)

        print(f"\n[Subscribed] {user.name} -> {plan.name}")
        self.billing_service.generate_invoice(self.subscription, current_date)

    def upgrade(self, new_plan):
        sub = self.subscription
        current_date = datetime.now()

        days_used = (current_date - sub.start_date).days
        remaining_days = 30 - days_used

        prorated = (remaining_days / 30) * new_plan.price

        print(f"\n[Upgrade] {sub.plan.name} -> {new_plan.name}")
        print(f"[Prorated Charge] ${round(prorated,2)}")

        sub.plan = new_plan
        self.billing_service.process_payment_with_retry(prorated, sub)

    def apply_coupon(self, coupon):
        self.subscription.coupon = coupon
        print(f"[Coupon Applied] {coupon.code}")

    def run_billing_cycle(self):
        current_date = datetime.now()

        if current_date >= self.subscription.next_billing_date:
            print("\n=== Billing Cycle ===")
            self.billing_service.generate_invoice(self.subscription, current_date)
            self.subscription.next_billing_date += timedelta(days=30)
        else:
            print("\n[Billing Not Due Yet]")


# ---------------------------
# Main Interactive Program
# ---------------------------

def main():
    print("=== Subscription Billing System ===")

    # User input
    user_id = int(input("Enter User ID: "))
    name = input("Enter Name: ")
    email = input("Enter Email: ")

    user = User(user_id, name, email)

    # Plan selection
    print("\nSelect Plan:")
    print("1. Free ($0)")
    print("2. Pro ($10)")
    print("3. Enterprise ($30)")

    choice = int(input("Enter choice: "))

    plans = {
        1: Plan("Free", 0),
        2: Plan("Pro", 10),
        3: Plan("Enterprise", 30)
    }

    selected_plan = plans.get(choice)

    service = SubscriptionService()
    service.subscribe(user, selected_plan)

    while True:
        print("\n--- Menu ---")
        print("1. Upgrade Plan")
        print("2. Apply Coupon")
        print("3. Run Billing Cycle")
        print("4. Show Status")
        print("5. Exit")

        option = int(input("Choose option: "))

        if option == 1:
            print("\nUpgrade To:")
            print("2. Pro ($10)")
            print("3. Enterprise ($30)")
            new_choice = int(input("Enter choice: "))
            service.upgrade(plans[new_choice])

        elif option == 2:
            code = input("Enter coupon code: ")
            ctype = input("Type (percent/flat): ")
            value = float(input("Value: "))
            coupon = Coupon(code, ctype, value)
            service.apply_coupon(coupon)

        elif option == 3:
            service.run_billing_cycle()

        elif option == 4:
            sub = service.subscription
            print("\n--- Subscription Status ---")
            print(f"User: {sub.user.name}")
            print(f"Plan: {sub.plan.name}")
            print(f"Status: {sub.status}")
            print(f"Next Billing: {sub.next_billing_date}")

        elif option == 5:
            print("Exiting...")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()