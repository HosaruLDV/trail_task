import pandas as pd


def calculate_tariff(file_name):
    data_frame = pd.read_json(file_name)
    data_frame['tariff'] = data_frame['highway_cost'] / data_frame['products'].apply(
        lambda x: sum(item['quantity'] for item in x))

    unique_warehouses = data_frame[['warehouse_name', 'tariff']].drop_duplicates()

    return data_frame


def field_sum_calculation(data):
    data_frame = data

    # Развертывание столбца 'products' и вычисление суммарных значений
    aggregated_data = data_frame['products'].explode().apply(pd.Series)
    aggregated_data['income'] = aggregated_data['quantity'] * aggregated_data['price']
    aggregated_data['expenses'] = aggregated_data['quantity'] * data_frame['tariff']
    aggregated_data['profit'] = aggregated_data['income'] - aggregated_data['expenses']
    # Группировка по товару и суммирование
    grouped_data = aggregated_data.groupby('product').sum().reset_index()
    # Переименование столбцов
    table = grouped_data[['product', 'quantity', 'income', 'expenses', 'profit']]

    return table


def profit_calculation(data):
    data_frame = data

    # Вычисление прибыли для каждого заказа
    data_frame['order_profit'] = data_frame['products'].apply(
        lambda x: sum(item['quantity'] * item['price'] for item in x)) + data_frame['tariff'] * data_frame[
                                     'products'].apply(lambda x: sum(item['quantity'] for item in x))

    # Создание таблицы с нужными столбцами 'order_id' и 'order_profit'
    table = data_frame[['order_id', 'order_profit']]
    return table


if __name__ == '__main__':
    file_path = 'trail_task.json'
    data_frame = calculate_tariff(file_path)
    unique_warehouses = data_frame[['warehouse_name', 'tariff']].drop_duplicates()
    print(unique_warehouses)
    print(field_sum_calculation(data_frame))
    print(profit_calculation(data_frame))
    data_frame = profit_calculation(data_frame)
    average_profit = data_frame['order_profit'].mean()
    print("Средняя прибыль заказов:", average_profit)
