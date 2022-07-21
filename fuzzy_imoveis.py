from skfuzzy import control as ctrl
import matplotlib.pyplot as plt
import numpy as np
import sys

# New Antecedent/Consequent objects hold universe variables and membership

mostrarGraficos = len(sys.argv) == 1

# tempo desde a construção

idade_imovel = ctrl.Antecedent(np.arange(0, 11, 1), 'idade_imovel')

# estado de conservação

estado = ctrl.Antecedent(np.arange(0, 11, 1), 'estado')

# a área do imóvel: 0 = muito pequeno; 10 = muito grande

area = ctrl.Antecedent(np.arange(0, 11, 1), 'area')

# se possui boa localização: perto do centro, seguro, etc

local = ctrl.Antecedent(np.arange(0, 11, 1), 'local')

# valor final do imóvel: de 20 mil a 1 milhão

valor = ctrl.Consequent(np.arange(20, 1000, 1), 'valor')

# Criando as variáveis qualitativas automaticamente

idade_imovel.automf(3)
estado.automf(3)
area.automf(7)
local.automf(5)
valor.automf(7)

# Visualizando os dados

if mostrarGraficos:
   idade_imovel.view()
   estado.view()
   area.view()
   local.view()
   valor.view()

# Definindo as regras de negócio

rules = []
rules.append(ctrl.Rule(local['poor'] | estado['poor'], valor['dismal']))
rules.append(ctrl.Rule(local['poor'] & area['dismal'] & estado['poor'], valor['dismal']))
rules.append(ctrl.Rule(local['poor'] & area['dismal'] | estado['poor'], valor['dismal']))
rules.append(ctrl.Rule(local['poor'] | area['poor'], valor['poor']))
rules.append(ctrl.Rule(area['poor'] | estado['poor'] | idade_imovel['poor'], valor['poor']))
rules.append(ctrl.Rule(local['poor'] & area['decent'] & estado['good'] & idade_imovel['poor'], valor['mediocre']))
rules.append(ctrl.Rule(local['average'] & area['excellent'] & estado['poor'], valor['mediocre']))
rules.append(ctrl.Rule(local['poor'] & estado['poor'], valor['poor']))
rules.append(ctrl.Rule(area['poor'] | idade_imovel['poor'], valor['mediocre']))
rules.append(ctrl.Rule(local['mediocre'] | area['mediocre'] & estado['average'], valor['mediocre']))
rules.append(ctrl.Rule(local['average'] | estado['good'] | idade_imovel['good'] | area['decent'], valor['average']))
rules.append(ctrl.Rule(local['good'] & area['excellent'], valor['good']))
rules.append(ctrl.Rule(local['good'] & area['good'] & estado['good'], valor['good']))
rules.append(ctrl.Rule(local['good'] & area['excellent'] & estado['good'] & idade_imovel['poor'], valor['good']))
rules.append(ctrl.Rule(local['average'] & area['average'] & estado['good'] & idade_imovel['average'], valor['decent']))
rules.append(ctrl.Rule(local['decent'] & area['good'], valor['decent']))
rules.append(ctrl.Rule(local['good'] & area['excellent'] & estado['good'] & idade_imovel['good'], valor['excellent']))


imovel_ctrl = ctrl.ControlSystem(rules)

# Criando a simulação para gerar o resultado

valor_imovel = ctrl.ControlSystemSimulation(imovel_ctrl)

# Definindo as variáveis de entrada

print("Responda cada pergunta com um valor de 0 a 10, sendo 0 muito baixo e 10 muito alto.\n")

valor_imovel.input['idade_imovel'] = int(input("Tempo de uso [0: antigo ... 10: novo]:\n> "))
valor_imovel.input['estado'] = int(input("Estado de conservação [0: ruim ... 10: bom]:\n> "))
valor_imovel.input['area'] = int(input("Tamanho do imóvel [0: pequeno ... 10: grande]:\n> "))
valor_imovel.input['local'] = int(input("Qualidade da localização (\
bairro, distância até o centro, etc) [0: ruim ... 10: boa]:\n> "))

# Calculando valor final

valor_imovel.compute()

# Mostrando valor final

print("Valor do imóvel: %d.000,00 R$" %(int(valor_imovel.output['valor'])-0))

# Plotando os gráficos na tela

if mostrarGraficos:
   valor.view(sim=valor_imovel)
   plt.show()

input("\npressione ENTER para sair")