import matplotlib.pyplot as plt 
import numpy as np 


x = [1,2,3,4,5] 
y = [3,3,3,3,3] 

plt.plot(x, y, label = "line 1", color='red', marker='o') 
plt.plot(y, x, label = "line 2") 
plt.plot(x, np.sin(x), label = "curve 1") 
plt.plot(x, np.cos(x), label = "curve 2") 

plt.title('unemployment rate vs year', fontsize=14)
plt.xlabel('year', fontsize=14)
plt.ylabel('unemployment rate', fontsize=14)


plt.legend() 
plt.grid(True)
plt.show()
  
#plt.plot(df['year'], df['unemployment_rate'], color='red', marker='o')
#plt.title('unemployment rate vs year', fontsize=14)
#plt.xlabel('year', fontsize=14)
#plt.ylabel('unemployment rate', fontsize=14)
#plt.grid(True)
#plt.show()"






