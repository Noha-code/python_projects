class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []
    
    def __str__(self):
        title = f"{self.name:*^30}\n"
        items=''
        for i in self.ledger:
            desc = i['description'][:23].ljust(23)
            amt = f"{i['amount']:.2f}"[:7].rjust(7)
            items += f"{desc}{amt}\n"
        total = f'Total: {self.get_balance():.2f}'
        return title + items + total


    def deposit(self, amount, description=''):
        self.ledger.append({'amount': amount, 'description': description})
    
    def withdraw(self, amount, description=''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.ledger.append({'amount': -amount, 'description': f"Transfer to {category.name}"})
            category.ledger.append({'amount': amount, 'description': f"Transfer from {self.name}"})
            return True
        return False
    
    def check_funds(self, amount):
        if amount > self.get_balance():
            return False
        return True

def create_spend_chart(categories):
    total_spendings=0
    chart_list=[]
    for category in categories:
        for item in category.ledger:
            if item['amount']<0:
                total_spendings+=abs(item['amount'])
    for category in categories:
        spendings = 0
        for item in category.ledger:
            if item['amount'] < 0:
                spendings += abs(item['amount'])
        prc=(spendings*100)/total_spendings
        rounded_prc = int(prc/10) * 10 
        chart_list.append({'category': category.name, 'percentage': rounded_prc})

    title = "Percentage spent by category"
    line = "    " + "-" * (len(chart_list) * 3 + 1)

    lines = []
    for i in range(100, -1, -10):
        x = ''
        for item in chart_list:
            if item['percentage'] >= i:
                x+=' o '
            else:
                x+='   '
        lines.append(str(i).rjust(3)+'|'+x+' ')

        names = []
        for i in range(max(len(cat['category']) for cat in chart_list)):
            row = "     " 
            for item in chart_list:
                if i < len(item['category']):
                    row += item['category'][i] + "  "
                else:
                    row += "   "
            names.append(row) 


    return title + '\n' + '\n'.join(lines) + '\n' + line + '\n' + '\n'.join(names)
