
import requests

def get_OHLC(pair):

    url = "https://api.kraken.com/0/public/OHLC?pair=" + pair

    payload = {}
    headers = {
       'Accept': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    return response.text


    # The function to add a number of columns inside an array
def adder(Data, times):
    
    for i in range(1, times + 1):
    
        new_col = np.zeros((len(Data), 1), dtype = float)
        Data = np.append(Data, new_col, axis = 1)
        
    return Data
# The function to delete a number of columns starting from an index
def deleter(Data, index, times):
    
    for i in range(1, times + 1):
    
        Data = np.delete(Data, index, axis = 1)
        
    return Data
    
# The function to delete a number of rows from the beginning
def jump(Data, jump):
    
    Data = Data[jump:, ]
    
    return Data
# Example of adding 3 empty columns to an array
my_ohlc_array = adder(my_ohlc_array, 3)
# Example of deleting the 2 columns after the column indexed at 3
my_ohlc_array = deleter(my_ohlc_array, 3, 2)
# Example of deleting the first 20 rows
my_ohlc_array = jump(my_ohlc_array, 20)
# Remember, OHLC is an abbreviation of Open, High, Low, and Close and it refers to the standard historic...       
            except IndexError:
                pass
            
    return Data
def atr(Data, lookback, high, low, close, where, genre = 'Smoothed'):
    
    # Adding the required columns
    Data = adder(Data, 1)
    
    # True Range Calculation
    for i in range(len(Data)):
        
        try:
            
            Data[i, where] =   max(Data[i, high] - Data[i, low],
                               abs(Data[i, high] - Data[i - 1, close]),
                               abs(Data[i, low] - Data[i - 1, close]))
            
        except ValueError:
            pass
        
    Data[0, where] = 0   
    
    if genre == 'Smoothed':
        
        # Average True Range Calculation
        Data = ema(Data, 2, lookback, where, where + 1)
    
    if genre == 'Simple':
    
        # Average True Range Calculation
        Data = ma(Data, lookback, where, where + 1)
    
    # Cleaning
    Data = deleter(Data, where, 1)
    Data = jump(Data, lookback)    
    return Data

def main():
    get_OHLC("BTCUSDT")


if __name__ == '__main__':
    main()
