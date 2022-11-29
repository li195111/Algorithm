'''
基本單位元素: 基因(Gene)
單位元素的集合: 染色體(Chromosome)
染色體的集合: 族群(Population)
初始化族群(Initial Population)
  確定族群大小(Population Size)，每一次的染色體有多少個
適應函數(Fitness Function)
  用來計算染色體(Chromosome)好壞的標準，用來篩選出適應程度較佳的染色體
  適應值(Fitness Value)就是用來顯示其適應程度的表現，不同的適應函數在不同的應用情境下對應到不同的計算方式
  設定適應值(Fitness Value)，當該染色體(Chromosome)的適應值達到目標適應值時，該組染色體(Chromosome)即為欲尋找的解
選擇(Selection)
  留下好的基因序列，使好的基因流傳下去
  根據不同的染色體所對應的適應值，當適應值越高，該群體有越高的機率被選取，以確保好的基因序列被保留
交配(Crossover)
  將兩兩染色體進行交配產生新的染色體，是否交配也會透過交配機率進行控制
  交配方式: 單點、多點
突變(Mutation)
  突變會在選中的染色體中對某些基因進行變化，以二進位說: 0->1, 1->0
  突變也會依據突變機率來改變
  為了避免最後的結果陷入區域最佳解的狀況
'''
from typing import List
import numpy as np


class Gene:
  NAME = 'GENE'
  def __init__(self, color:str, color_display:bool, display:bool) -> None:
    self.__color = color
    self.__color_display = color_display
    self.__display = display
  
  def __repr__(self) -> str:
    if self.color_display:
      return f'{self.color} {self.NAME}'
    return f'{self.NAME}'
  
  @property
  def color(self):
    return self.__color
  
  @property
  def color_display(self):
    return self.__color_display
  
  @property
  def display(self):
    return self.__display

class Hair(Gene):
  NAME = 'Hair'
  def __init__(self, color: str, color_display: bool, display: bool) -> None:
    super().__init__(color, color_display, display)

class Eyes(Gene):
  NAME = 'Eyes'
  def __init__(self, color: str, color_display: bool, display: bool) -> None:
    super().__init__(color, color_display, display)


colors = ['red','green','blue','brown','black','white','none']
color_display = [True, False]

hair_gene_set = [Hair(color, color_display=True, display=True) for color in colors]
eyes_gene_set = [Eyes(color, color_display=True, display=True) for color in colors]
gene_set = hair_gene_set + eyes_gene_set
print(gene_set)
# init_size = 50
# init_genes = np.concatenate([np.random.choice(colors, (init_size,1)),
#                              np.random.choice(gene_set, (init_size,1))],1)
# init_genes = np.array(list(map(lambda x: ' '.join(x), init_genes)))
# init_gene_set = set(init_genes)
# init_gene_set_size = len(init_gene_set)
# print(init_gene_set)

# chro_size = len(gene_set)
# popu_size = 23


class Chromosome:
  def __init__(self, size:int) -> None:
    self.size = size
    self.genetics:List[Gene] = []
  
  def add(self, gene:Gene):
    if len(self.genetics) < self.size:
      self.genetics.append(gene)
  
  def fitness_value(self, func):
    return func(self)

class Population:
  def __init__(self, size:int) -> None:
    self.size = size
    self.chromosomes:List[Chromosome] = []
  
  def add(self, chromosome:Chromosome):
    if len(self.chromosomes) < self.size:
      self.chromosomes.append(chromosome)
  