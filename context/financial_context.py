from schemas.financial_profile import FinancialProfile
from context.demo_data_provider import load_user


class FinancialContext:

    def get_user(self, user_id: str) -> FinancialProfile:
        data = load_user(user_id)

        return FinancialProfile.model_validate(data)

    def get_income(self, user_id: str):
        user = self.get_user(user_id)
        return user.income

    def get_expenses(self, user_id: str):
        user = self.get_user(user_id)
        return user.expenses

    def get_assets(self, user_id: str):
        user = self.get_user(user_id)
        return user.assets

    def get_liabilities(self, user_id: str):
        user = self.get_user(user_id)
        return user.liabilities

    def get_goals(self, user_id: str):
        user = self.get_user(user_id)
        return user.goals

    def get_insurance(self, user_id: str):
        user = self.get_user(user_id)
        return user.insurance

    def get_risk_profile(self, user_id: str):
        user = self.get_user(user_id)
        return user.risk_profile