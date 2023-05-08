from lark import Lark, Tree, Transformer
from lark.visitors import CollapseAmbiguities

my_grammar = """
start: simple_sentence

simple_sentence: [ADVERB ", "] noun_phrase verb_phrase

noun_phrase: SUB_PRONOUN | PROPER_NOUN_PHRASE | ARTICLE [ADJECTIVE] NOUN [ADJECTIVE] [prep_phrase*]
verb_phrase: (verb_struct [ADVERB] | verb_struct [ADVERB] direct_object_phrase | verb_struct [ADVERB] ADJECTIVE) [prep_phrase*]
prep_phrase: PREP [ARTICLE | PARTITIVE] ([ADJECTIVE] NOUN [ADJECTIVE] | PREP_PRONOUN) 
direct_object_phrase: PARTITIVE [ADJECTIVE] NOUN [ADJECTIVE] | ARTICLE [ADJECTIVE] NOUN [ADJECTIVE] | PROPER_NOUN_PHRASE | POSSESSIVE_ADJ [ADJECTIVE] NOUN [ADJECTIVE]



ARTICLE: "um"i | "uma"i | "uns"i | "o"i | "a"i | "os"i | "as"i | "ao"i | "à"i | "às"i
PARTITIVE: "do" | "da" | "dos" | "das"

NOUN: "americano" | "americanos" | "americana" | "americanas" | "amigo" | "ano" | "anos" | "árvore" | "árvores" | "hoje"
| "muito" | "cerveja" | "cervejas" | "carne" | "café" | "cafés" | "sofá" | "cozinha"
| "amanhã"
| "água" | "escola" | "escolas" | "elefante" | "elefantes" | "criança" | "crianças" | "esposa"
| "mulher" | "homens" | "filho" | "filha" | "filhas"
| "menino" | "meninos" | "gelo" | "gelo"
| "hora" | "ontem" | "homem" | "homens"
| "marido" | "mãe" | "minuto"
| "cama"
| "pássaro" | "pássaros" | "computador"
| "pizza" | "pizzas" | "pai" | "peixe" | "porco" | "frango"
| "segundo" | "segundos"
| "semana" | "semanas"
| "chá" | "banheiro"
| "carro" | "carros"
| "zoológico"

SUB_PRONOUN: "Eu"i | "Tu"i | "Ele"i | "Ela"i | "Nós"i | "Vós"i | "Eles"i | "Elas"i | "Isso"i
| "Este"i | "Essa"i | "Esse"i | "Estes"i | "Estas"i | "Esses"i | "Aquilo"i | "Aquele"i | "Aquela"i | "Aqueles"i | "Aquelas"i | "Aqueloutro"i | "Aqueloutra"i

PREP_PRONOUN: "mim" | "ti" | "ele" | "ela" | "nós" | "vós" | "eles" | "elas"
PROPER_NOUN_PHRASE: "Jake"i | "França"i

ADJECTIVE: "americano" | "americana" | "divertido" | "divertida" | "americanos" | "americanas" | "divertidos" | "divertidas"
| "bom" | "boa" | "bons" | "boas"
| "difícil" | "difíceis"
| "fácil" | "fáceis"
| "grande" | "grandes"
| "mau" | "má" | "maus" | "más"
| "pequeno" | "


%import common.NUMBER
%import common.WS
%ignore WS
"""

parser = Lark(my_grammar, ambiguity = 'explicit')

print("\nBem-vindo ao analisador francês, escrito por (Welcome to the Porthugese parsing)\n")
print("Digite uma frase para ver se ela pode ser analisada! (Enter a sentence to see if it can be parsed! - Note: do not use characters ./?/!)")
print("Digite 'info' para ver mais informações sobre este programa! (Enter 'info' to see more information about this program!)")
print("Digite 'exemplo' para ver alguns exemplos! (Enter 'example' to see some examples!)")
print("Ou digite a palavra 'sair' para sair. (Or, enter the word 'quitter' to exit.)\n")

sentence = input()

while (sentence != "sair"):
  if (sentence == "info"):
     print("""
     //////////////////////////////////////////////////////////////////////////////////////////
     This program receives sentences through standard input and attempts to parse them using the grammar I have defined.
     Sentences should be made up of a noun phrase followed by a verb phrase.
     /////////////////////////////////////////////////////////////////////////////////////////////
     """)
        
  elif (sentence == "exemplo"):
     
        print("""
        1: 'Eu gosto de pizza' vs. 'Eu gosto da pizza'

        Este exemplo ilustra uma certa distinção entre o francês e o inglês. As palavras da primeira frase se traduzem diretamente em 
        "I like pizza", mas a frase está gramaticalmente incorreta. Em francês, os substantivos geralmente exigem um artigo ou frase 
         partitiva antes. Essa frase se torna correta adicionando "da" antes de pizza. As tentativas de análise para ambas as frases 
         estão mostradas abaixo.
    
        """)

        try:
           sentence = "Eu gosto de pizza"
           print(parser.parse(sentence).pretty())
        except:
           print("Não há análise válida para '" + sentence + "'. (There is no valid parse for '" + sentence + "'.)")

        try:
          sentence = "Eu gosto da pizza"
          print("\nEu gosto da pizza")
          print(parser.parse(sentence).pretty())
        except:
          print("Não há análise válida para '" + sentence + "'. (There is no valid parse for '" + sentence + "'.)\n\n")
    
        print("""
    2: 'As crianças querem veem o elefante no zoológico' vs. 'As crianças querem ver o elefante no zoológico'

    Este exemplo mostra que um verbo conjugado não deve ser seguido por outro verbo conjugado. A frase acima se traduz em "The children 
    want to see the elephant at the zoo", mas apenas a segunda frase está escrita corretamente. Isso ocorre porque a segunda frase usa 
    a estrutura correta de seguir o verbo conjugado "querem" pelo verbo infinitivo "ver". As tentativas de análise para ambas as frases 
    estão mostradas abaixo.
    
    """)

        try:
           sentence = "As crianças querem veem o elefante no zoológico"
           print(parser.parse(sentence).pretty())
        except:
           print("Não há análise válida para '" + sentence + "'. (There is no valid parse for '" + sentence + "'.)\n")

        try:
           sentence = "As crianças querem ver o elefante no zoológico"
           print("As crianças querem ver o elefante no zoológico")
           print(parser.parse(sentence).pretty())
        except:
           print("Não há análise válida para '" + sentence + "'. (There is no valid parse for '" + sentence + "'.)\n\n")

        print("""
              3: 'Os pássaros nas árvores'

            Este exemplo mostra que uma frase não pode consistir apenas de uma frase nominal e, portanto, esta frase não tem análise. 
            Atualmente, a frase se traduz em "the birds in the trees". Como desafio, tente adicionar algo a essa frase para transformá-la 
            em uma frase completa! Em seguida, teste-a no analisador. (Uma opção é escrever esta frase: "Os pássaros nas árvores querem 
            beber água.")
    
             """)

        try:
           sentence = "Os pássaros nas árvores"
           print("Os pássaros nas árvores")
           print(parser.parse(sentence).pretty())
        except:
           print("Não há análise válida para " + sentence + " . (There is no valid parse for '" + sentence + "'.)\n\n")

print("Digite uma frase para ver se ela pode ser analisada! (Enter a sentence to see if it can be parsed! - Note: do not use character ./?/!)")
print("Digite 'info' para ver mais informações sobre este programa! (Enter 'info' to see more information about this program!)")
print("Digite 'exemplo' para ver alguns exemplos! (Enter 'example' to see some examples!)")
print("Ou, digite 'sair' para sair. (Or, enter the word 'sair' to exit.)\n")
sentence = input()
