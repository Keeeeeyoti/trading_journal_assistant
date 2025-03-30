from ai_parser import parse_with_ollama_two
from sql_handler import write_trade, read_trades


result = parse_with_ollama_two("I bought 100 shares of BTC at 50000")
print(f"Data type is {type(result)}")
print(result)
write_trade(result["entities"])
