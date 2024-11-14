// Функция для выполнения конвертации при изменении входных данных
function convertCurrency() {
  const fromCurrency = document.getElementById("from-currency").value;
  const toCurrency = document.getElementById("to-currency").value;
  const amount = parseFloat(document.getElementById("amount").value);

  if (isNaN(amount) || amount <= 0) {
      document.getElementById("result").textContent = "Please enter a valid amount.";
      document.getElementById("converted-amount").value = '';
      return;
  }

  // Отправляем запрос на сервер Flask
  fetch("http://127.0.0.1:5000/api/convert", {
      method: "POST",
      headers: {
          "Content-Type": "application/json"
      },
      body: JSON.stringify({
          fromCurrency: fromCurrency,
          toCurrency: toCurrency,
          amount: amount
      })
  })
  .then(response => response.json())
  .then(data => {
      if (data.result) {
          // Выводим результат в поле для конвертированной суммы
          document.getElementById("converted-amount").value = data.result.toFixed(2);
          document.getElementById("result").textContent = `Converted: ${data.result.toFixed(2)} ${toCurrency}`;
      } else {
          document.getElementById("result").textContent = data.error || "Conversion failed.";
      }
  })
  .catch(error => {
      console.error("Error:", error);
      document.getElementById("result").textContent = "An error occurred. Please try again.";
  });
}

// Добавляем события для отслеживания изменений
document.getElementById("from-currency").addEventListener("change", convertCurrency);
document.getElementById("to-currency").addEventListener("change", convertCurrency);
document.getElementById("amount").addEventListener("input", convertCurrency);
