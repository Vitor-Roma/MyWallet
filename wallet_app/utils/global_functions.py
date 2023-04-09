from _decimal import Decimal


def round_percent_string_to_decimal(value):
    return round(Decimal(value[:-1].replace(',', '.')), 2)


def category_color_dict(category):
    color_dict = {
        'Recebimentos': '#00ff00',
        'Compras': '#ff0000',
        'Cartão': '#7FFF00',
        'Rendimentos': '#ffff00',
        'Reembolso': '#6699ff',
        'Moradia': '#cc6699',
        'Farmácia': '#ff00ff',
        'Contas': '#4d4dff',
        'Mercado': '#ff9900',
        'Alimentação': '#00ffff',
        'Viagem': '#F08080',
        'Saúde': '#20B2AA',
        'Estudo': '#9370DB',
        'Mãe': '#FF6347',
        'Transporte': '#000080',
        'Jogo': '#228B22',
        'Lazer': '#00FA9A',
        'Pet': '#9932CC',
        'Saldo +/-': '#000000',
        'Outros': '#808080',
        'Transferência': '#FFFF00'
    }
    return color_dict[category]


def category_icon_dict():
    icons = {
        "Recebimentos": "fas fa-money-bill-wave",
        "Compras": "fas fa-shopping-cart",
        "Cartão": "fas fa-credit-card",
        "Rendimentos": "fas fa-chart-line",
        "Reembolso": "fas fa-money-bill-wave",
        "Moradia": "fas fa-home",
        "Farmácia": "fas fa-medkit",
        "Contas": "fas fa-file-invoice-dollar",
        "Mercado": "fas fa-shopping-basket",
        "Alimentação": "fas fa-utensils",
        "Viagem": "fas fa-plane",
        "Saúde": "fas fa-heartbeat",
        "Estudo": "fas fa-book",
        "Mãe": "fas fa-female",
        "Transporte": "fas fa-car",
        "Jogo": "fab fa-steam",
        "Lazer": "fas fa-dungeon",
        "Pet": "fas fa-cat",
        "Saldo +/-": "fas fa-money-check-alt",
        "Outros": "fas fa-globe",
        "Transferência": "fas fa-exchange-alt"
    }
    return icons