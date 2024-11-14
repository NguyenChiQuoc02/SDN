import pandas as pd
import pickle
import matplotlib.pyplot as plt

class ModelInference:

    def __init__(self, model_path='model1.pkl', data_path='ddos.csv'):
        # Tải mô hình đã huấn luyện
        with open(model_path, 'rb') as file:
            self.model = pickle.load(file)
        print("Mô hình đã được tải thành công.")

        self.new_data = pd.read_csv(data_path)
        self.new_data.iloc[:, 2] = self.new_data.iloc[:, 2].str.replace('.', '')
        self.new_data.iloc[:, 3] = self.new_data.iloc[:, 3].str.replace('.', '')
        self.new_data.iloc[:, 5] = self.new_data.iloc[:, 5].str.replace('.', '')

        self.X_new = self.new_data.iloc[:, :-1].values.astype('float64')
        self.y_new = self.new_data.iloc[:, -1].values

    def predict(self):

        y_pred = self.model.predict(self.X_new)

        normal_count = sum(y_pred == 0)
        ddos_count = sum(y_pred == 1)

        for i, prediction in enumerate(y_pred):
            if prediction == 0:
                print(f"Dữ liệu mẫu {i+1} thuộc lớp: Normal")
            else:
                print(f"Dữ liệu mẫu {i+1} thuộc lớp: DDoS")

        plt.bar(['Normal', 'DDoS'], [normal_count, ddos_count], color=['blue', 'red'])
        plt.title('Phân bố dự đoán: Normal vs DDoS')
        plt.xlabel('Lớp')
        plt.ylabel('Số lượng mẫu')
        plt.show()

def main():

    inference = ModelInference(model_path='model.pkl', data_path='normal_ddos.csv')
    inference.predict()

if __name__ == "__main__":
    main()
