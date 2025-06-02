from flask import jsonify
import json
from models import Questionario, Sessao, Pergunta, Alternativa, User 
from extensions import db
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

questionarios = [
    {
      "titulo": "Questionário M-CHAT (Modified Checklist for Autism in Toddlers)",
      "descricao": "Triagem para risco de Transtorno do Espectro Autista em crianças de 16 a 30 meses.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Modified Checklist for Autism in Toddlers, Revised (M-CHAT-R)",
          "autores": "Robins, D. L., Fein, D., Barton, M. L., & Green, J. A.",
          "ano": 2001
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "M-CHAT (Modified Checklist for Autism in Toddlers)",
          "descricao": "Lista de perguntas para pais ou cuidadores.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "A criança sorri para você quando você sorri para ela?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela gosta de brincar de \"esconde-esconde\" ou de jogos de esconder?",
              "tipo_resposta": "booleano",
              "ordem": 2,
              "is_obrigatoria": True,
              "metodo_pontuacao": "soma_item",
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela prefere brincar sozinha, sem interagir com outras crianças?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela está interessada em interagir com outras crianças ou adultos?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela se aproxima de você para ser abraçada ou tocada?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela aponta para objetos, como brinquedos ou comida, para mostrar que está interessada?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela usa gestos para se comunicar (como acenar ou apontar)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela tenta chamar sua atenção apontando ou usando algum outro gesto?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela fala palavras ou frases, como “mamãe” ou “papai”?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela responde ao seu nome quando você chama?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela olha para objetos ou pessoas quando você está olhando ou falando sobre eles?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela roda objetos (como rodas de brinquedos) por um longo tempo?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela tem algum comportamento repetitivo, como bater palmas ou balançar o corpo?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela se fixa em uma parte do objeto, como uma roda ou uma parte específica de um brinquedo?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela demonstra interesse intenso por um tipo específico de objeto, como rodas ou engrenagens?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela se interessa por objetos ou pessoas fora de seu campo de visão (olhando para algo distante)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 16,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela gosta de observar objetos ou pessoas em movimento (como carros, animais ou pessoas andando)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 17,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela tenta explorar objetos de uma maneira mais profunda, como observá-los de perto ou mexer neles?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 18,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela parece indiferente quando você entra na sala ou sai dela?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 19,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela se assusta facilmente com sons altos ou luzes brilhantes?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 20,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela tem interesse por texturas, como esfregar coisas contra a pele ou se balançar de maneira repetitiva?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 21,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela gosta de olhar para objetos brilhantes ou em movimento, como luzes piscando?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 22,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Ela já aprendeu a andar ou a correr sem ajuda?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 23,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "ADOS-2 (Autism Diagnostic Observation Schedule, Second Edition) - Módulo 1",
      "descricao": "Questionário adaptado com base nas áreas de observação do ADOS-2 Módulo 1 (para crianças de 2 a 5 anos com pouca ou nenhuma fala). As perguntas refletem comportamentos observados durante a avaliação.",
      "versao": "Second Edition",
      "fontes_literatura": [
        {
          "titulo": "Autism Diagnostic Observation Schedule, Second Edition (ADOS-2) Manual (Part I): Modules 1-4",
          "autores": "Lord, C., Rutter, M., DiLavore, P. C., Risi, S., Gotham, K., & Bishop, S. L.",
          "journal": "Manual publicado pela Western Psychological Services (WPS)",
          "ano": 2012,
          "volume": None,
          "numero": None,
          "paginas": None
        },
        {
          "titulo": "The Autism Diagnostic Observation Schedule—Generic: A standard measure of social and communication deficits associated with the spectrum of autism",
          "autores": "Lord, C., Rutter, M., DiLavore, P. C., Cook, E. H., Leventhal, B. L., DiLavore, P. C., Pickles, A., & Rutter, M.",
          "journal": "Journal of Autism and Developmental Disorders",
          "ano": 2000,
          "volume": 30,
          "numero": 3,
          "paginas": "205-223"
        },
        {
          "titulo": "Autism Diagnostic Observation Schedule: ADOS-2",
          "autores": "Lord, C., Rutter, M., DiLavore, P. C., Risi, S., Gotham, K., & Bishop, S. L.",
          "journal": "Los Angeles, CA: Western Psychological Services",
          "ano": 2012,
          "volume": None,
          "numero": None,
          "paginas": None
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Comunicação Não Verbal",
          "descricao": "Perguntas relacionadas à comunicação não verbal da criança durante as atividades.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "A criança utiliza gestos para se comunicar (ex: apontar para pedir algo)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança tenta mostrar objetos ao examinador por iniciativa própria?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança entrega objetos ao examinador para interação?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança olha para onde o examinador aponta?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Respostas aos Outros",
          "descricao": "Perguntas relacionadas à forma como a criança responde às tentativas de comunicação do examinador.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "A criança responde quando o examinador chama seu nome?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança imita ações ou sons feitos pelo examinador?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Interação Social Recíproca",
          "descricao": "Perguntas relacionadas à capacidade da criança de compartilhar atenção e interagir.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "A criança faz contato visual com o examinador durante as interações?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança parece desfrutar de brincadeiras interativas com o examinador?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança busca compartilhar seus interesses com o examinador?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Brincadeira e Interesse",
          "descricao": "Perguntas relacionadas ao comportamento da criança durante a brincadeira e seus interesses.",
          "ordem": 4,
          "perguntas": [
            {
              "texto": "A criança brinca com brinquedos de forma funcional e variada?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança demonstra interesse em uma variedade de brinquedos ou atividades?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança demonstra brincadeira simbólica ou imaginativa?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Comportamentos Repetitivos e Interesses Restritos",
          "descricao": "Perguntas relacionadas a comportamentos repetitivos, estereotipados ou interesses incomuns.",
          "ordem": 5,
          "perguntas": [
            {
              "texto": "A criança apresenta movimentos repetitivos do corpo (ex: balançar, girar)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança demonstra manipulação incomum de objetos (ex: alinhar, girar partes)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança tem um interesse muito forte ou fixo em um objeto ou tópico específico?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Respostas a Estímulos Sensoriais",
          "descricao": "Perguntas relacionadas à forma como a criança reage a estímulos sensoriais.",
          "ordem": 6,
          "perguntas": [
            {
              "texto": "A criança demonstra reações incomuns a sons (ex: tapar os ouvidos, ignorar)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A criança demonstra interesse incomum por texturas ou objetos (ex: tocar repetidamente)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "CARS (Childhood Autism Rating Scale)",
      "descricao": "Questionário adaptado com base nos 15 itens da Childhood Autism Rating Scale (CARS) para avaliar a gravidade do autismo em crianças.",
      "versao": "",
      "fontes_literatura": [
        {
          "titulo": "Toward objective classification of childhood autism: Childhood Autism Rating Scale (CARS)",
          "autores": "Schopler, E., Reichler, R. J., DeVellis, R. F., & Daly, K.",
          "journal": "Journal of Autism and Developmental Disorders",
          "ano": 1980,
          "volume": 10,
          "numero": 1,
          "paginas": "91-103"
        },
        {
          "titulo": "Childhood Autism Rating Scale–Second Edition (CARS-2)",
          "autores": "Schopler, E., Van Bourgondien, M. E., Wellman, G. J., & Love, S. R.",
          "journal": "Manual publicado pela Western Psychological Services (WPS)",
          "ano": 2010,
          "volume": None,
          "numero": None,
          "paginas": None
        },
        {
          "titulo": "Comparison of DSM-III-R and Childhood Autism Rating Scale diagnoses of autism",
          "autores": "Van Bourgondien, M. E., & Schopler, E.",
          "journal": "Journal of Autism and Developmental Disorders",
          "ano": 1993,
          "volume": 23,
          "numero": 2,
          "paginas": "343-352"
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Itens do CARS",
          "descricao": "Avaliação dos 15 itens que observam diversos aspectos do comportamento da criança.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "A criança demonstra relação com as pessoas de forma atípica?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança imita ações, sons ou palavras de forma atípica?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança apresenta respostas emocionais inadequadas?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança apresenta uso do corpo de forma peculiar?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra uso peculiar de objetos?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança apresenta adaptação a mudanças de forma atípica?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra respostas visuais atípicas?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra respostas auditivas atípicas?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra respostas gustativas, olfativas e táteis atípicas?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança apresenta medo ou nervosismo atípicos?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra comunicação verbal atípica?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra comunicação não verbal atípica?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança apresenta nível de atividade motora atípico?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra nível e consistência de respostas intelectuais atípicos?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança apresenta impressão geral de que é autista?",
              "tipo_resposta": "personalizado",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4",
                  "valor": 4.0,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "CISS (Childhood Autism Spectrum Disorder Questionnaire)",
      "descricao": "Questionário para identificar comportamentos e características associadas ao Transtorno do Espectro Autista (TEA) em crianças.",
      "versao": None,
      "fontes_literatura": [],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Interações Sociais",
          "descricao": "Avalia a habilidade da criança em interagir com outras pessoas, incluindo a resposta social, empatia e reciprocidade nas interações.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "A criança evita olhar nos olhos das pessoas durante interações sociais.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança tem dificuldade em entender as emoções de outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança tem dificuldades em fazer ou manter amizades com outras crianças.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra pouco ou nenhum interesse em interagir com outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança parece ter dificuldade em responder de forma adequada a interações sociais.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Comunicação",
          "descricao": "Avalia a capacidade de comunicação verbal e não verbal da criança, incluindo o uso de linguagem para se comunicar de forma eficaz e adequada.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "A criança usa palavras ou frases incompletas para expressar necessidades.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança usa gestos para se comunicar de forma consistente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança tem dificuldades para iniciar uma conversa ou fazer perguntas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança tem dificuldades em manter uma conversa, interrompendo ou não seguindo o fluxo da troca.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança tem um vocabulário muito limitado ou usa palavras de forma repetitiva e rígida.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Comportamentos Repetitivos e Restritos",
          "descricao": "Observa padrões de comportamento repetitivo ou restrito, que são típicos no espectro autista.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "A criança exibe comportamentos repetitivos, como balançar o corpo, bater as mãos ou girar objetos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança se concentra obsessivamente em objetos ou atividades específicas, excluindo outras opções.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança demonstra resistência a mudanças na rotina ou em atividades diárias.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança exibe comportamentos estereotipados, como alinhar objetos ou repetir ações de forma ritualizada.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança evita ou não demonstra interesse por brincadeiras imaginativas ou de faz de conta.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente ocorre.",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes ocorre.",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ocorre.",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre ocorre.",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Questionário VABS-II - Comunicação",
      "descricao": "Avaliação do domínio de Comunicação do Vineland Adaptive Behavior Scales, Second Edition.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Vineland Adaptive Behavior Scales, Second Edition",
          "autores": "Sparrow, S. S., Cicchetti, D. V., & Balla, D. A.",
          "ano": 2005
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Expressão Verbal",
          "descricao": "Avaliação das habilidades de expressão da linguagem verbal.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "A pessoa usa palavras isoladas para se comunicar?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue formar frases simples de duas ou três palavras?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa utiliza frases completas para expressar suas necessidades?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue descrever eventos ou objetos usando a fala?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa faz perguntas para obter informações?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue contar histórias simples?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa vocabulário variado e apropriado para a idade?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue expressar seus sentimentos verbalmente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue participar de conversas, mantendo o tópico?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue iniciar conversas de forma apropriada?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa a fala para comentar sobre o ambiente ou o que está acontecendo?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue responder a perguntas de forma clara e relevante?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa utiliza pronomes (eu, você, ele/ela) corretamente na fala?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue usar a fala para expressar concordância ou discordância?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue adaptar sua fala ao contexto e ao ouvinte?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Compreensão da Linguagem",
          "descricao": "Avaliação das habilidades de compreensão da linguagem verbal.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "A pessoa demonstra entender seu próprio nome quando chamado?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa reage a palavras familiares como 'mamãe' e 'papai'?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa segue comandos simples de uma etapa ('Sente', 'Vem cá')?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue identificar objetos comuns quando nomeados ('bola', 'carro')?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa entende perguntas simples como 'Onde está?'?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa segue comandos de duas etapas ('Pegue a bola e coloque na caixa')?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra entender conceitos como 'grande' e 'pequeno'?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa responde a perguntas com 'sim' ou 'não' corretamente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa compreende preposições simples como 'em', 'debaixo', 'ao lado'?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa entende perguntas que envolvem 'quem', 'o quê' e 'onde'?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue seguir instruções verbais em um grupo?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra entender conversas simples entre outras pessoas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue entender o significado de diferentes tons de voz?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra compreender instruções mais complexas com múltiplas etapas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue entender nuances da linguagem, como sarcasmo ou ironia (se apropriado para a idade)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Habilidade Não Verbal",
          "descricao": "Avaliação das habilidades de comunicação não verbal.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "A pessoa usa contato visual para se comunicar ou interagir?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa gestos simples como apontar para indicar o que quer?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa compreende gestos simples de outras pessoas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa expressões faciais para comunicar emoções?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa interpreta corretamente as expressões faciais de outras pessoas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa a linguagem corporal (postura, movimentos) para comunicar?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa entende a linguagem corporal de outras pessoas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa sinais convencionais (como balançar a cabeça para 'sim' ou 'não')?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa desenhos ou escrita para se comunicar (se apropriado para a idade)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa tecnologia assistiva para se comunicar (se aplicável)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue seguir indicações não verbais?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa a comunicação não verbal para expressar suas preferências?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa tenta se comunicar mesmo quando não consegue usar palavras?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa a comunicação não verbal para iniciar interações sociais?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa usa uma variedade de formas não verbais para se comunicar?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Questionário VABS-II - Vida Doméstica / Habilidades Práticas",
      "descricao": "Avaliação do domínio de Vida Doméstica / Habilidades Práticas do Vineland Adaptive Behavior Scales, Second Edition.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Vineland Adaptive Behavior Scales, Second Edition",
          "autores": "Sparrow, S. S., Cicchetti, D. V., & Balla, D. A.",
          "ano": 2005
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Vida Doméstica / Habilidades Práticas",
          "descricao": "Avaliação das habilidades relacionadas à vida doméstica e tarefas práticas.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "A pessoa consegue se alimentar sozinha de forma independente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue vestir e despir roupas sozinha?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue realizar higiene pessoal básica (escovar os dentes, lavar o rosto e as mãos)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa ajuda a guardar seus pertences (roupas, brinquedos, etc.)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue preparar refeições simples (fazer um sanduíche, esquentar algo no micro-ondas)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa ajuda em tarefas domésticas como arrumar a mesa ou lavar louça?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue usar eletrodomésticos simples como a televisão ou o controle remoto?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue seguir uma rotina diária (por exemplo, hora de acordar, refeições, dormir)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue usar o banheiro de forma independente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue identificar e usar objetos domésticos comuns (copo, prato, talheres)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue ajudar a organizar o ambiente doméstico?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra entender regras básicas de segurança doméstica?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue realizar pequenas tarefas de manutenção doméstica (por exemplo, trocar uma lâmpada, se apropriado para a idade)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue utilizar o telefone para fazer ligações simples (se apropriado para a idade)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra responsabilidade com suas tarefas domésticas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Questionário VABS-II - Socialização",
      "descricao": "Avaliação do domínio de Socialização do Vineland Adaptive Behavior Scales, Second Edition.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Vineland Adaptive Behavior Scales, Second Edition",
          "autores": "Sparrow, S. S., Cicchetti, D. V., & Balla, D. A.",
          "ano": 2005
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Socialização",
          "descricao": "Avaliação das habilidades de interação e comportamento social.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "A pessoa interage com outras pessoas de forma apropriada para a idade?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra interesse em brincar ou participar de atividades com outras pessoas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue esperar sua vez em jogos ou atividades?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa segue as regras de jogos ou atividades em grupo?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra empatia ou preocupação com os sentimentos dos outros?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue iniciar e manter conversas com outras pessoas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue fazer amigos?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra compreender as normas sociais básicas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue lidar com conflitos ou desentendimentos de forma apropriada?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra respeito pelas propriedades dos outros?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue se adaptar a diferentes situações sociais?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue compreender e responder a dicas sociais?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa participa de atividades sociais e comunitárias (se apropriado para a idade)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra consciência dos sentimentos e necessidades dos outros?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue manter relacionamentos sociais positivos?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Questionário VABS-II - Motor",
      "descricao": "Avaliação do domínio Motor do Vineland Adaptive Behavior Scales, Second Edition.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Vineland Adaptive Behavior Scales, Second Edition",
          "autores": "Sparrow, S. S., Cicchetti, D. V., & Balla, D. A.",
          "ano": 2005
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Motor",
          "descricao": "Avaliação das habilidades motoras grossas e finas.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "A pessoa consegue andar sem ajuda?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue correr?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue subir e descer escadas com ou sem apoio?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue pular com os dois pés?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue pegar uma bola com as mãos?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue arremessar uma bola?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue usar as mãos para manipular objetos pequenos?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue segurar um lápis ou caneta corretamente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue desenhar formas simples (círculo, linha)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue abotoar e desabotoar roupas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue usar tesoura para cortar papel?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue amarrar os sapatos (se apropriado para a idade)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue virar páginas de um livro?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa consegue construir algo simples com blocos ou brinquedos de montar?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A pessoa demonstra coordenação motora adequada para a idade em atividades diárias?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Questionário ABC (Autism Behavior Checklist)",
      "descricao": "Avaliação de comportamentos autistas.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Autism Behavior Checklist",
          "autores": "Krug, D. A., Arick, J. R., & Almond, P.",
          "ano": 1980
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "ABC (Autism Behavior Checklist)",
          "descricao": "Lista de comportamentos associados ao autismo.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Evita olhar nos olhos de outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Não responde ao ser chamado pelo nome.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Não demonstra interesse por outras crianças ou adultos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Não reage ao toque ou à aproximação de outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Prefere brincar sozinho e evita interações sociais.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Não utiliza palavras ou frases para se comunicar.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Não aponta para objetos ou pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A criança tem dificuldade em compreender instruções simples.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Não utiliza gestos (como acenar ou apontar).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Usa palavras repetidamente sem significado (ecolalia).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Realiza movimentos repetitivos (como bater as mãos, balançar o corpo).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Fica obcecado por objetos ou partes de objetos (por exemplo, girar rodas ou focar em padrões).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Demonstra resistência a mudanças na rotina.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Repetição excessiva de atividades ou comportamentos (como bater ou repetir a mesma ação).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Mantém um interesse intenso por atividades específicas (por exemplo, vídeos, músicas, objetos específicos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em coordenar movimentos (como correr ou brincar com brinquedos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 16,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem episódios de agressividade (como bater, morder, empurrar).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 17,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Apresenta comportamentos autolesivos (como morder-se ou se bater).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 18,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Apresenta dificuldades significativas em atividades motoras finas (como desenhar ou usar talheres).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 19,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em manter a postura ou equilíbrio (como ficar em pé ou andar).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 20,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Parece não ter consciência dos sentimentos dos outros.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 21,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Não compartilha brinquedos ou objetos com os outros.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 22,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em participar de brincadeiras de faz de conta.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 23,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Prefere brincar com objetos do que com pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 24,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em entender piadas ou sarcasmo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 25,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Usa outras pessoas como ferramentas para obter o que quer.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 26,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em entender regras sociais.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 27,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Não inicia conversas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 28,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em manter uma conversa.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 29,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Fala sobre um assunto de forma repetitiva.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 30,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Faz perguntas repetidamente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 31,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem um vocabulário limitado para a idade.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 32,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Usa pronomes de forma incorreta (ex: 'você' para 'eu').",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 33,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em expressar suas próprias ideias ou opiniões.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 34,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em entender perguntas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 35,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Imita os outros sem entender o contexto.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 36,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em iniciar uma conversa quando quer algo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 37,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem maneirismos incomuns com as mãos ou dedos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 38,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Anda na ponta dos pés.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 39,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem movimentos corporais rígidos ou tensos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 40,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em imitar movimentos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 41,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Deixa cair objetos com frequência.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 42,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em usar utensílios (colher, garfo).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 43,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em vestir-se sozinho.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 44,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em usar o banheiro sozinho.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 45,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em dormir sozinho.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 46,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem acessos de raiva.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 47,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Chora sem motivo aparente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 48,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ri sem motivo aparente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 49,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Parece não sentir dor.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 50,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Reage de forma exagerada a barulhos altos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 51,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem medo de objetos ou situações comuns sem motivo aparente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 52,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em se concentrar em uma tarefa.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 53,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "É excessivamente ativo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 54,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em ficar parado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 55,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem comportamentos impulsivos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 56,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem padrões de sono irregulares.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 57,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre ou quase sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Avaliação do Early Start Denver Model (ESDM)",
      "descricao": "Escalas e itens principais avaliados no Early Start Denver Model (ESDM).",
      "versao": None,
      "fontes_literatura": [
        {
          "titulo": "Early Start Denver Model for young children with autism: A randomized controlled trial",
          "autores": "Dawson, G., Rogers, S., Munson, J., Smith, M., Winter, J., Greenson, J., ... & Varley, J.",
          "ano": 2010
        },
        {
          "titulo": "Long-term outcomes of early intervention in 6-year-old children with autism spectrum disorder",
          "autores": "Estes, A., Munson, J., Dawson, G., Rogers, S. J., & Winter, J.",
          "ano": 2015
        },
        {
          "titulo": "Early Start Denver Model for young children with autism: Promoting language, learning, and engagement",
          "autores": "Rogers, S. J., & Dawson, G.",
          "ano": 2010
        },
        {
          "titulo": "An early start for your child with autism: Using everyday activities to help kids connect, communicate, and learn",
          "autores": "Rogers, S. J., Dawson, G., & Vismara, L. A.",
          "ano": 2012
        },
        {
          "titulo": "Behavioral treatments in autism spectrum disorder: What do we know?",
          "autores": "Vismara, L. A., & Rogers, S. J.",
          "ano": 2010
        },
        {
          "titulo": "Telehealth for early autism: What the research shows",
          "autores": "Vismara, L. A., Rogers, S. J., & Young, G. S.",
          "ano": 2010
        },
        {
          "titulo": "The Early Start Denver Model: A case study of an innovative practice",
          "autores": "Vismara, L., & Rogers, S.",
          "ano": 2008
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Desenvolvimento Cognitivo",
          "descricao": "Avalia a capacidade da criança de aprender, resolver problemas e realizar atividades cognitivas básicas.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Atenção ao ambiente: A criança consegue manter sua atenção em estímulos, como objetos ou pessoas, por períodos adequados?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não sustenta atenção)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (atenção focada e mantida por períodos adequados)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Habilidade de resolver problemas: A criança pode resolver problemas simples de forma independente, como montar um quebra-cabeça ou realizar atividades práticas?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não demonstra habilidade de resolver problemas)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (resolve problemas com facilidade e de forma independente)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Imitação: A criança consegue imitar ações ou comportamentos demonstrados por outras pessoas? (exemplo: imitar gestos ou palavras)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não imita)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (imita de forma precisa e contextualizada)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Flexibilidade cognitiva: A criança consegue adaptar sua forma de pensar quando ocorre uma mudança ou uma novidade?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (dificuldade em lidar com mudanças)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (demonstra flexibilidade cognitiva e se adapta com facilidade)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Desenvolvimento Social e de Comunicação",
          "descricao": "Avalia a capacidade da criança de se comunicar, expressar emoções e interagir socialmente com outros.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Respostas sociais e emocionais: A criança responde a interações sociais com adultos e outras crianças de forma apropriada (como sorrir, manter contato visual, responder a toques)?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não responde socialmente)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (responde de forma consistente e apropriada a estímulos sociais)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Imitação social: A criança pode imitar comportamentos sociais, como acenar para despedir-se, dar um beijo ou fazer gestos específicos?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não imita comportamentos sociais)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (imita uma ampla gama de comportamentos sociais de forma precisa)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Comunicação verbal e não verbal: A criança utiliza palavras ou gestos para se comunicar suas necessidades e desejos (exemplo: apontar, fazer gestos, usar palavras)?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não utiliza comunicação verbal ou não verbal)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (utiliza comunicação verbal e não verbal adequadas e variadas)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Interações com pares: A criança interage com outras crianças de forma apropriada, compartilhando brinquedos ou engajando-se em brincadeiras paralelas ou cooperativas?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não interage com outras crianças)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (engaja-se ativamente e de forma adequada nas interações sociais)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Compreensão de normas sociais: A criança entende normas sociais básicas, como esperar a vez, cumprimentar com palavras e expressões adequadas, ou reconhecer sinais sociais de desconforto (exemplo: compreender quando alguém está triste)?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não demonstra compreensão)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (compreende e segue normas sociais de maneira espontânea)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Desenvolvimento Motor e Autocontrole",
          "descricao": "Abrange a avaliação das habilidades motoras grossas e finas da criança, além de sua capacidade de autorregulação emocional e comportamental.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "Coordenação motora grossa: A criança consegue realizar atividades físicas como correr, pular, subir escadas, e manter equilíbrio de forma adequada à sua idade?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não consegue realizar atividades motoras)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (realiza atividades motoras com facilidade e adequação)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Coordenação motora fina: A criança é capaz de usar suas mãos para realizar tarefas finas, como pegar objetos pequenos, desenhar ou encaixar peças de brinquedos?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não consegue realizar tarefas motoras finas)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (realiza tarefas motoras finas com facilidade e precisão)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Autocontrole emocional: A criança consegue regular suas emoções e comportamentos de forma adequada, como se acalmar quando está frustrada ou controlar impulsos?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não consegue controlar impulsos ou emoções)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (demonstra autorregulação emocional adequada à situação)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Interação motor-social: A criança consegue se engajar em atividades que exigem coordenação motora com um componente social, como brincar de esconde-esconde ou empurrar um carrinho de brinquedo para outra criança?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "nivel_desenvolvimento",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 (não participa de brincadeiras motoras com outros)",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 (engaja-se com facilidade e com controle nas interações motoras)",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Ritvo Autism and Asperger Diagnostic Scale-Revised (RAADS-R)",
      "descricao": "Escala de avaliação para ajudar na identificação de características do Transtorno do Espectro Autista (TEA) em adultos e adolescentes.",
      "versao": None,
      "fontes_literatura": [
        {
          "titulo": "The Ritvo Autism Asperger Diagnostic Scale-Revised (RAADS-R): A Scale to Assist the Diagnosis of Autism Spectrum Disorder in Adults: An International Validation Study",
          "autores": "Ritvo, R. A., Ritvo, E. R., Guthrie, D., Yuwiler, A., Ritvo, M., & Weisbender, L.",
          "ano": 2011,
          "publicacao": "Journal of Autism and Developmental Disorders, 41(8), 1076–1089",
          "doi": "10.1007/s10803-010-1133-5"
        },
        {
          "titulo": "A scale to assist the diagnosis of Autism and Asperger's disorder in Adults (RAADS): A pilot study",
          "autores": "Ritvo, R., Ritvo, E., Guthrie, D., Yuwiler, A., Ritvo, M., & Weisbender, L.",
          "ano": 2008,
          "publicacao": "Journal of Autism and Developmental Disorders, 38(2), 213–223",
          "doi": None
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Comunicação",
          "descricao": "Este domínio avalia a capacidade do indivíduo de se comunicar de forma eficiente e apropriada, incluindo tanto a comunicação verbal quanto a não verbal.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Tendo conversas, eu sou desinteressado nas interações com os outros.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho dificuldade em compreender expressões faciais e linguagem corporal.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu frequentemente falo sem parar, independentemente de uma conversa ou de estar sendo ouvido.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho dificuldade em entender piadas ou ironias.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu frequentemente não sei como manter uma conversa (por exemplo, não sei quando é minha vez de falar).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu costumo usar palavras e frases de filmes e televisão em conversas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Às vezes falo muito alto ou muito baixo e não percebo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tenho dificuldade em entender o significado de algumas frases, como \"você é a menina dos meus olhos\".",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu sempre noto como a comida fica na minha boca. Isso é mais importante para mim do que o gosto dela.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Às vezes ofendo os outros ao dizer o que estou pensando, mesmo que não seja minha intenção.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu me concentro nos detalhes em vez da ideia geral.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tomo as coisas muito literalmente, então muitas vezes perco o que as pessoas estão tentando dizer.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "As pessoas me dizem que dou muitos detalhes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu sou frequentemente surpreendido quando os outros me dizem que fui rude.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não consigo entender quando alguém está flertando comigo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não consigo entender quando alguém diz uma coisa, mas quer dizer outra.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 16,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não sei quando é minha vez de falar ou de ouvir quando estou conversando com alguém.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 17,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho dificuldade em entender como as outras pessoas se sentem quando estamos conversando.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 18,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não consigo entender quando alguém está sendo sarcástico.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 19,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não consigo imaginar como seria estar no lugar de outra pessoa.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 20,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Interações Sociais",
          "descricao": "Este domínio avalia a capacidade do indivíduo de se relacionar com outras pessoas, estabelecendo e mantendo interações sociais adequadas.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Eu evito interações sociais ou as encontro muito difíceis.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não entendo as convenções sociais (por exemplo, quando alguém está entediado ou desconfortável, eu não percebo).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho dificuldade em fazer ou manter amigos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu prefiro estar sozinho ou com poucas pessoas ao invés de grandes grupos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não entendo ou sei como expressar sentimentos em relação a outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu consigo me colocar no lugar das outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 3.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 1.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 0.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Só gosto de conversar com pessoas que tenham os mesmos interesses que os meus.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Sinto falta dos meus melhores amigos ou familiares quando ficamos separados por muito tempo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 3.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 1.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 0.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Prefiro sair para comer em um restaurante sozinho do que com alguém que conheço.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Os outros me consideram estranho ou diferente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu entendo quando os amigos precisam ser consolados.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 3.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 1.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 0.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu gosto de ter uma conversa com várias pessoas, por exemplo, em volta de uma mesa de jantar, na escola ou no trabalho.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 3.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 1.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 0.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "É muito difícil para mim entender quando alguém está envergonhado ou com ciúmes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu gosto de ter amigos próximos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 3.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 1.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 0.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu sou considerado um tipo de pessoa compassiva.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 3.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 1.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 0.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu consigo me dar bem com outras pessoas seguindo um conjunto de regras específicas que me ajudam a parecer normal.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 16,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "É difícil para mim descobrir o que as outras pessoas esperam de mim.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 17,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu gosto de estar sozinho o máximo que posso.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 18,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu sou considerado um solitário por aqueles que melhor me conhecem.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 19,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu me sinto muito confortável em namorar ou estar em situações sociais com outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 20,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 3.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 1.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 0.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Comportamentos e Interesses Restritos e Repetitivos",
          "descricao": "Este domínio avalia a presença de comportamentos repetitivos, interesses restritos ou a adesão rígida a rotinas.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "Eu sou muito fixado em certas atividades ou tópicos e não me interesso por outras coisas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu fico muito incomodado quando minha rotina é interrompida ou quando as coisas não acontecem do jeito que eu espero.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho movimentos repetitivos ou comportamentos repetitivos (por exemplo, balançar o corpo, bater as mãos, andar de um lado para o outro).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho interesses incomuns ou excêntricos que consomem muito do meu tempo (por exemplo, colecionar objetos ou se fixar em um tema específico).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu faço movimentos ou sons repetitivos sem perceber ou sem ter um propósito claro.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu só gosto de pensar e falar sobre algumas coisas que me interessam.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu me concentro nos detalhes em vez da ideia geral.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu fico extremamente chateado quando a maneira como gosto de fazer as coisas é repentinamente mudada.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho rituais ou rotinas que preciso seguir.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho sido fascinado por algumas coisas (como números, datas, sequências ou padrões) desde que eu era criança.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu gosto que as coisas sejam exatamente iguais dia após dia e até mesmo pequenas mudanças em minhas rotinas me chateiam.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu nunca fui interessado no que a maioria das pessoas que conheço considera interessante.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu gosto de colecionar coisas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu gosto de planejar as coisas com muito cuidado antes de fazê-las.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho que seguir um caminho familiar quando vou a algum lugar ou posso ficar muito confuso e chateado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Processamento Sensorial",
          "descricao": "Este domínio avalia a maneira como o indivíduo percebe e reage aos estímulos sensoriais, como luz, som, tato, etc.",
          "ordem": 4,
          "perguntas": [
            {
              "texto": "Eu tenho reações intensas a estímulos sensoriais (como sons altos, luzes brilhantes ou certos tecidos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu tenho dificuldades em perceber ou entender estímulos sensoriais, como não perceber se alguém está falando ou se algo está acontecendo ao meu redor.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu evito certos lugares ou situações por causa de estímulos sensoriais (por exemplo, evitar multidões ou lugares barulhentos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu sou excessivamente sensível ao toque ou ao contato físico.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu me sinto confortável ou até fico atraído por estímulos sensoriais incomuns (por exemplo, luzes piscando, sons repetitivos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Já me disseram que sou desajeitado ou descoordenado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Sou muito sensível à sensação das roupas na minha pele. A sensação das roupas no corpo é mais importante do que o modelo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Às vezes tenho que cobrir meus ouvidos para bloquear ruídos dolorosos (como aspiradores de pó ou pessoas falando demais ou muito alto).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "A mesma coisa (como roupas ou temperaturas) pode parecer muito diferente para mim em momentos diferentes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Algumas texturas comuns que não incomodam os outros parecem muito ofensivas quando tocam minha pele.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Às vezes, coisas que deveriam ser dolorosas não são (por exemplo, quando me machuco ou queimo a mão no fogão).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O mesmo som, cor ou textura pode mudar repentinamente de muito sensível para muito fraco.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Se eu estou em um lugar onde há muitos cheiros, texturas para sentir, ruídos ou luzes brilhantes, eu me sinto ansioso ou assustado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não gosto de ser abraçado ou segurado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Eu não consigo tolerar coisas que eu não gosto (como cheiros, texturas, sons ou cores).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Às vezes",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Adult ADHD Self-Report Scale (ASRS-v1.1) Symptom Checklist",
      "descricao": "Instrumento de rastreamento para sintomas de Transtorno do Déficit de Atenção com Hiperatividade (TDAH) em adultos.",
      "versao": "v1.1",
      "fontes_literatura": [
        {
          "titulo": "Med Clin North Am",
          "autores": "Schweitzer JB, et al.",
          "ano": 2001,
          "publicacao": "85(3):10-11, 757-777",
          "doi": None
        },
        {
          "titulo": "Attention Deficit Hyperactivity Disorder: A Handbook for Diagnosis and Treatment",
          "autores": "Barkley RA",
          "ano": 1998,
          "publicacao": "2nd ed.",
          "doi": None
        },
        {
          "titulo": "Am J Psychiatry",
          "autores": "Biederman J, et al.",
          "ano": 1993,
          "publicacao": "150:1792-1798",
          "doi": None
        },
        {
          "titulo": "Diagnostic and Statistical Manual of Mental Disorders, Fourth Edition, Text Revision",
          "autores": "American Psychiatric Association",
          "ano": 2000,
          "publicacao": "Washington, DC: American Psychiatric Association; 85-93.",
          "doi": None
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Parte A",
          "descricao": "As seis perguntas mais preditivas de sintomas consistentes com TDAH em adultos.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Com que frequência você tem dificuldade em prestar atenção ou se concentrar quando está fazendo algum trabalho que é enfadonho ou repetitivo?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4,
                  "is_shaded": True
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5,
                  "is_shaded": True
                }
              ]
            },
            {
              "texto": "Com que frequência você tem dificuldade em manter a atenção quando está fazendo algo interessante?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4,
                  "is_shaded": True
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5,
                  "is_shaded": True
                }
              ]
            },
            {
              "texto": "Com que frequência você se sente inquieto ou agitado?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4,
                  "is_shaded": True
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5,
                  "is_shaded": True
                }
              ]
            },
            {
              "texto": "Com que frequência você tem dificuldade em relaxar e se acalmar quando está com tempo livre?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4,
                  "is_shaded": True
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5,
                  "is_shaded": True
                }
              ]
            },
            {
              "texto": "Com que frequência você evita ou adia começar algo que você tem que fazer porque se sente entediado ou desinteressado?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4,
                  "is_shaded": True
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5,
                  "is_shaded": True
                }
              ]
            },
            {
              "texto": "Com que frequência você tem dificuldade em se organizar quando tem que fazer várias tarefas?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4,
                  "is_shaded": True
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5,
                  "is_shaded": True
                }
              ]
            }
          ]
        },
        {
          "titulo": "Parte B",
          "descricao": "Perguntas adicionais sobre sintomas de TDAH em adultos.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Com que frequência você tem dificuldade em se lembrar de compromissos ou obrigações?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você evita ou adia começar tarefas que exigem muito pensamento?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você se mexe ou se contorce na sua cadeira quando tem que ficar sentado por muito tempo?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você se sente excessivamente ativo e compelido a fazer coisas, como se estivesse 'ligado'?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você se vê fazendo ou dizendo coisas impulsivamente que depois se arrepende?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você tem dificuldade em esperar sua vez em situações em que isso é necessário?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você interrompe os outros quando eles estão falando?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você tem dificuldade em ficar quieto quando precisa?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você perde coisas ou tem dificuldade em encontrar as coisas em casa ou no trabalho?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você se distrai por seus próprios pensamentos ou por coisas ao seu redor?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você tem dificuldade em deixar as coisas de lado ou parar de fazer algo que deveria?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            },
            {
              "texto": "Com que frequência você tem dificuldade em se concentrar em algo, como ler ou conversar, sem se distrair?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Às vezes",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "3 = Frequentemente",
                  "valor": 3.0,
                  "ordem": 4
                },
                {
                  "texto": "4 = Muito frequentemente",
                  "valor": 4.0,
                  "ordem": 5
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "SNAP-IV para Crianças e Adolescentes",
      "descricao": "Questionário SNAP-IV para avaliação de sintomas de TDAH em crianças e adolescentes, baseado nos critérios do DSM-IV.",
      "versao": "IV",
      "fontes_literatura": [
        {
          "titulo": "Manual de Diagnóstico e Estatística de Transtornos Mentais - IV Edição (DSM-IV)",
          "autores": "Associação Americana de Psiquiatria",
          "ano": None,
          "publicacao": None,
          "doi": None
        }
      ],
      "is_active": True,
      "observacoes": "Este questionário é apenas um ponto de partida para o levantamento de possíveis sintomas primários do TDAH. O diagnóstico correto e preciso só pode ser feito através de uma longa anamnese (entrevista) com um profissional médico especializado (psiquiatra, neurologista, neuropediatra).",
      "sessoes": [
        {
          "titulo": "Desatenção (Itens 1 a 9)",
          "descricao": "Avaliar a frequência dos seguintes comportamentos. A presença de pelo menos 6 itens marcados como 'Bastante' ou 'Demais' sugere mais sintomas de desatenção que o esperado.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Não consegue prestar muita atenção a detalhes ou comete erros por descuido nos trabalhos da escola ou tarefas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldade de manter a atenção em tarefas ou atividades de lazer.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Parece não estar ouvindo quando se fala diretamente com ele.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Não segue instruções até o fim e não termina deveres de escola, tarefas ou obrigações.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldade para organizar tarefas e atividades.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Evita, não gosta ou se envolve contra a vontade em tarefas que exigem esforço mental prolongado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Extravia objetos necessários para tarefas ou atividades.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Distrai-se facilmente por estímulos externos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "É esquecido em atividades diárias.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            }
          ]
        },
        {
          "titulo": "Hiperatividade/Impulsividade (Itens 10 a 18)",
          "descricao": "Avaliar a frequência dos seguintes comportamentos. A presença de pelo menos 6 itens marcados como 'Bastante' ou 'Demais' sugere mais sintomas de hiperatividade e impulsividade que o esperado.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Remexe as mãos ou os pés ou se contorce na cadeira.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Levanta da cadeira em sala de aula ou em outras situações em que se espera que fique sentado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Corre ou escala em demasia em situações em que isto é inadequado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldade de brincar ou se envolver em atividades de lazer calmamente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 13,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Está sempre 'a mil' ou muitas vezes age como se estivesse 'a todo vapor'.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 14,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Fala em demasia.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 15,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Dá respostas precipitadas antes que as perguntas tenham sido terminadas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 16,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldade de esperar sua vez.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 17,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Interrompe os outros ou se intromete (por exemplo: intromete-se nas conversas, jogos, etc.).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 18,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "SNAP-IV para Adultos",
      "descricao": "Questionário SNAP-IV para avaliação de sintomas de TDAH em adultos, considerando dificuldades em organização, impulsividade e funcionamento social/profissional.",
      "versao": "IV",
      "fontes_literatura": [
        {
          "titulo": "Apresentação de uma versão em português para uso no Brasil do instrumento MTA-SNAP-IV de avaliação de sintomas de transtorno do déficit de atenção/hiperatividade e sintomas de transtorno desafiador e de oposição.",
          "autores": "MATTOS et al",
          "ano": 2005
        },
        {
          "titulo": "Avaliação do transtorno de déficit de atenção/ hiperatividade em adultos (TDAH): uma revisão de literatura.",
          "autores": "LOPES, R.M.F.; NASCIMENTO, R.F.L.; BANDEIRA, D.R.",
          "ano": 2005
        },
        {
          "titulo": "Escala Snap-IV.",
          "autores": "KONESKI, J.",
          "ano": 2021
        },
        {
          "titulo": "O questionário SNAP-IV como auxiliar psicopedagógico no diagnóstico PRELIMINAR do Transtorno de déficit de atenção e hiperatividade (TDAH)",
          "autores": "Gabrielli Teresa Gadens Marcon; Helena Venites Sardagna; Dolores Schussler",
          "ano": 2016
        },
        {
          "titulo": "Parent SNAP-IV rating of attention-deficit/hyperactivity disorder: accuracy in a clinical sample of ADHD, validity, and reliability in a Brazilian sample",
          "autores": "Costa DS, de Paula JJ, Malloy-Diniz LF, Romano-Silva MA, Miranda DM",
          "ano": 2019
        },
        {
          "titulo": "O SNAP-IV é um questionário de domínio público, de livre acesso, que inclui os 18 itens correspondentes aos sintomas do crit",
          "autores": "Dr. Julio Koneski",
          "ano": 2021
        }
      ],
      "is_active": True,
      "observacoes": "Interpretação dos Resultados: O cálculo e a interpretação seguem a mesma lógica da versão infantil. Pontuações moderadas ou severas indicam a necessidade de avaliação clínica.\n\nPróximos Passos para Adultos:\n- Consulta com psiquiatra ou neuropsicólogo especializado em TDAH adulto.\n- Adoção de técnicas organizacionais e de gerenciamento de tempo.\n- Possível intervenção medicamentosa ou terapia cognitivo-comportamental.\n- Adaptação de rotinas para melhor produtividade e controle emocional.",
      "sessoes": [
        {
          "titulo": "Seção 1: Déficit de Atenção (Inatenção)",
          "descricao": "Avalie a frequência com que você experimenta as seguintes dificuldades.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Tem dificuldade em manter o foco em tarefas longas (trabalho, estudos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Distrai-se facilmente com conversas, celulares ou ruídos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Esquece compromissos ou prazos importantes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldade em organizar tarefas e administrar o tempo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Perde objetos importantes (chaves, carteira, documentos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Procrastina frequentemente tarefas que exigem esforço mental contínuo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Começa várias tarefas sem concluir nenhuma.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Sente-se sobrecarregado ao lidar com múltiplas responsabilidades.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Esquece detalhes de conversas ou instruções recentes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Alterna entre interesses rapidamente sem aprofundamento.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 2: Hiperatividade e Impulsividade",
          "descricao": "Avalie a frequência com que você experimenta os seguintes comportamentos.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Sente-se inquieto e tem dificuldade em ficar parado por muito tempo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Interrompe falas ou responde antes das perguntas serem concluídas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Fala excessivamente, sem perceber quando está monopolizando a conversa.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Toma decisões impulsivas sem avaliar as consequências.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldade em esperar sua vez em filas ou discussões.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Envolve-se em atividades de risco (dirigir rápido, gastos excessivos, decisões impulsivas).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Muda de emprego ou projeto frequentemente devido à falta de interesse.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Sente-se constantemente inquieto, como se precisasse estar sempre ocupado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldades em relaxar e aproveitar momentos de lazer.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Busca estímulos frequentes para evitar o tédio.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "SNAP-IV para Adultos",
      "descricao": "Questionário SNAP-IV para avaliação de sintomas de TDAH em adultos, considerando dificuldades em organização, impulsividade e funcionamento social/profissional.",
      "versao": "IV",
      "fontes_literatura": [
        {
          "titulo": "Apresentação de uma versão em português para uso no Brasil do instrumento MTA-SNAP-IV de avaliação de sintomas de transtorno do déficit de atenção/hiperatividade e sintomas de transtorno desafiador e de oposição.",
          "autores": "MATTOS et al",
          "ano": 2005
        },
        {
          "titulo": "Avaliação do transtorno de déficit de atenção/ hiperatividade em adultos (TDAH): uma revisão de literatura.",
          "autores": "LOPES, R.M.F.; NASCIMENTO, R.F.L.; BANDEIRA, D.R.",
          "ano": 2005
        },
        {
          "titulo": "Escala Snap-IV.",
          "autores": "KONESKI, J.",
          "ano": 2021
        },
        {
          "titulo": "O questionário SNAP-IV como auxiliar psicopedagógico no diagnóstico PRELIMINAR do Transtorno de déficit de atenção e hiperatividade (TDAH)",
          "autores": "Gabrielli Teresa Gadens Marcon; Helena Venites Sardagna; Dolores Schussler",
          "ano": 2016
        },
        {
          "titulo": "Parent SNAP-IV rating of attention-deficit/hyperactivity disorder: accuracy in a clinical sample of ADHD, validity, and reliability in a Brazilian sample",
          "autores": "Costa DS, de Paula JJ, Malloy-Diniz LF, Romano-Silva MA, Miranda DM",
          "ano": 2019
        },
        {
          "titulo": "O SNAP-IV é um questionário de domínio público, de livre acesso, que inclui os 18 itens correspondentes aos sintomas do crit",
          "autores": "Dr. Julio Koneski",
          "ano": 2021
        }
      ],
      "is_active": True,
      "observacoes": "Interpretação dos Resultados: O cálculo e a interpretação seguem a mesma lógica da versão infantil. Pontuações moderadas ou severas indicam a necessidade de avaliação clínica.\n\nPróximos Passos para Adultos:\n- Consulta com psiquiatra ou neuropsicólogo especializado em TDAH adulto.\n- Adoção de técnicas organizacionais e de gerenciamento de tempo.\n- Possível intervenção medicamentosa ou terapia cognitivo-comportamental.\n- Adaptação de rotinas para melhor produtividade e controle emocional.",
      "sessoes": [
        {
          "titulo": "Seção 1: Déficit de Atenção (Inatenção)",
          "descricao": "Avalie a frequência com que você experimenta as seguintes dificuldades.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Tem dificuldade em manter o foco em tarefas longas (trabalho, estudos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Distrai-se facilmente com conversas, celulares ou ruídos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Esquece compromissos ou prazos importantes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldade em organizar tarefas e administrar o tempo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Perde objetos importantes (chaves, carteira, documentos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Procrastina frequentemente tarefas que exigem esforço mental contínuo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Começa várias tarefas sem concluir nenhuma.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Sente-se sobrecarregado ao lidar com múltiplas responsabilidades.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Esquece detalhes de conversas ou instruções recentes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Alterna entre interesses rapidamente sem aprofundamento.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 2: Hiperatividade e Impulsividade",
          "descricao": "Avalie a frequência com que você experimenta os seguintes comportamentos.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Sente-se inquieto e tem dificuldade em ficar parado por muito tempo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Interrompe falas ou responde antes das perguntas serem concluídas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Fala excessivamente, sem perceber quando está monopolizando a conversa.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Toma decisões impulsivas sem avaliar as consequências.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldade em esperar sua vez em filas ou discussões.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Envolve-se em atividades de risco (dirigir rápido, gastos excessivos, decisões impulsivas).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Muda de emprego ou projeto frequentemente devido à falta de interesse.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Sente-se constantemente inquieto, como se precisasse estar sempre ocupado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Tem dificuldades em relaxar e aproveitar momentos de lazer.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            },
            {
              "texto": "Busca estímulos frequentes para evitar o tédio.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_media_sessao",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "0 = Nem um pouco",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1 = Só um pouco",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "2 = Bastante",
                  "valor": 2.0,
                  "ordem": 3,
                  "limiar_positivo": True
                },
                {
                  "texto": "3 = Demais",
                  "valor": 3.0,
                  "ordem": 4,
                  "limiar_positivo": True
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Escala de Avaliação de Comportamento de Achenbach (CBCL) para Avaliação de TDAH",
      "descricao": "Escala baseada na CBCL/6-18 para rastreamento de sintomas de TDAH em crianças e adolescentes.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Child Behavior Checklist for Ages 6-18 (CBCL/6-18)",
          "autores": "Achenbach, T. M., & Rescorla, L. A.",
          "ano": 2001
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Parte I: Sintomas de Desatenção",
          "descricao": "Questões relacionadas a sintomas de desatenção.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Tem dificuldade em prestar atenção por muito tempo?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Não parece escutar o que lhe dizem?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Não segue instruções e não termina tarefas escolares, domésticas ou no trabalho (não por oposição ou falha em entender as instruções)?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Tem dificuldade em organizar tarefas e atividades?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Evita, não gosta ou reluta em se envolver em tarefas que exigem esforço mental constante (como trabalhos escolares ou de casa)?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Perde coisas necessárias para tarefas ou atividades (por exemplo, brinquedos, trabalhos escolares, lápis, livros ou ferramentas)?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Distrai-se facilmente com estímulos externos?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "É esquecido em atividades diárias (por exemplo, fazer as tarefas)?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Parece não pensar antes de agir?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Tem dificuldade em manter o foco quando está brincando?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Parece ter a mente em outro lugar, mesmo quando não há distração por perto?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Tem dificuldade em seguir regras e instruções detalhadas?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            }
          ]
        },
        {
          "titulo": "Parte II: Sintomas de Hiperatividade e Impulsividade",
          "descricao": "Questões relacionadas a sintomas de hiperatividade e impulsividade.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Remexe ou batuca as mãos ou os pés ou se contorce na cadeira?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Levanta da cadeira em situações em que se espera que fique sentado?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Corre ou escala em demasia em situações em que isso não é apropriado (em adolescentes, pode ser sentimento de agitação)?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Tem dificuldade em brincar ou se envolver em atividades de lazer de forma calma?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Está frequentemente “a mil” ou agindo como se estivesse \"com um motor\"?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Fala em demasia?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Responde perguntas antes que elas tenham sido completadas?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Tem dificuldade em esperar a sua vez?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Interrompe ou se intromete em conversas ou jogos de outros?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Age sem pensar nas consequências?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Tem dificuldade em ficar parado durante atividades em grupo?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Pega objetos de outras pessoas sem pedir permissão?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            }
          ]
        },
        {
          "titulo": "Parte III: Problemas de Conduta (Opcional)",
          "descricao": "Questões relacionadas a problemas de conduta.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "Discute com adultos?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Desafia ativamente ou se recusa a obedecer às regras dos adultos?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Irrita deliberadamente outras pessoas?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Culpa os outros por seus erros ou mau comportamento?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "É frequentemente birrento, zangado ou ressentido?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "É vingativo ou rancoroso?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Mente ou quebra promessas?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Rouba em casa ou fora de casa?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Não é verdade",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Algumas vezes ou um pouco verdade",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente ou muito verdade",
                  "valor": 2.0,
                  "ordem": 3
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Bateria Neuropsicológica de Avaliação de Funções Executivas (NEPSY-II) para Avaliação de TDAH",
      "descricao": "Escala baseada em subescalas da NEPSY-II para avaliar funções executivas relacionadas ao TDAH em indivíduos de 3 a 16 anos.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "NEPSY-II: A Developmental Neuropsychological Assessment, Second Edition",
          "autores": "Korkman, M., Kirk, U., & Kemp, S. L.",
          "ano": 2007
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Atenção Sustentada e Controle Inibitório",
          "descricao": "Questões relacionadas à capacidade de manter a atenção e controlar impulsos.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "O indivíduo consegue manter sua atenção em uma tarefa por um período longo sem se distrair?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele/ela demonstra dificuldade em interromper atividades para iniciar novas tarefas, mesmo quando instruído?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Quando distraído, ele/ela tem dificuldades em voltar rapidamente ao foco inicial?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Durante atividades que exigem paciência, ele/ela se mostra impaciente frequentemente?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo tem problemas para aguardar sua vez em situações de jogo ou atividades em grupo?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "2. Memória de Trabalho",
          "descricao": "Questões relacionadas à capacidade de reter e manipular informações.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Ele/ela consegue reter informações enquanto trabalha em uma tarefa que exige múltiplos passos?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo tem dificuldades em realizar tarefas de memória de curto prazo, como lembrar de um número enquanto executa outra tarefa?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo se distrai facilmente ao tentar lembrar informações importantes durante atividades acadêmicas ou diárias?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele/ela tem problemas em organizar a memória de forma eficiente para realizar tarefas complexas?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo tem dificuldades para alternar entre diferentes informações ou tarefas com eficiência?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "3. Flexibilidade Cognitiva e Planejamento",
          "descricao": "Questões relacionadas à capacidade de adaptar o pensamento e planejar ações.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "O indivíduo consegue adaptar rapidamente seu plano de ação quando ocorre uma mudança inesperada na tarefa ou situação?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele/ela tem dificuldades para encontrar diferentes maneiras de resolver um problema ou tarefa?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo prefere seguir um único caminho ao invés de explorar alternativas, mesmo quando novas soluções poderiam ser mais eficientes?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele/ela tem dificuldades em reestruturar seu comportamento ou abordagem quando confrontado com um obstáculo?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo tem dificuldade em planejar com antecedência atividades ou tarefas importantes?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "4. Habilidades de Controle e Impulsividade",
          "descricao": "Questões relacionadas ao controle de reações e impulsos.",
          "ordem": 4,
          "perguntas": [
            {
              "texto": "O indivíduo tem dificuldades para controlar reações impulsivas em situações emocionais ou sociais?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele/ela comete erros impulsivos durante tarefas que exigem atenção e concentração?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo frequentemente interrompe outras pessoas ou age sem pensar em como suas ações podem afetar os outros?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele/ela tem dificuldades em manter um comportamento socialmente adequado em ambientes estruturados, como sala de aula ou reuniões?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo é frequentemente impulsivo em atividades que exigem paciência, como esperar em filas ou seguir regras?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "5. Raciocínio e Tomada de Decisão",
          "descricao": "Questões relacionadas à capacidade de raciocinar e tomar decisões.",
          "ordem": 5,
          "perguntas": [
            {
              "texto": "O indivíduo tende a tomar decisões rapidamente, sem considerar as consequências ou as informações disponíveis?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele/ela toma decisões baseadas em informações inadequadas ou parciais?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo consegue analisar uma situação de forma lógica e tomar uma decisão bem fundamentada?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Quando confrontado com múltiplas opções, o indivíduo tem dificuldade em escolher a mais vantajosa ou eficaz?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo é influenciado por emoções imediatas ao tomar decisões importantes?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Entrevista Diagnóstica Estruturada para Transtornos de TDAH (K-SADS)",
      "descricao": "Entrevista estruturada para avaliar e diagnosticar TDAH em crianças e adolescentes (6-18 anos) com base nos critérios do DSM-5.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "The Kiddie-Schedule for Affective Disorders and Schizophrenia (K-SADS)",
          "autores": "Kaufman, J., Birmaher, B., Brent, D., Rao, U., Flynn, C., Moreci, P., Williamson, D., & Ryan, N. D.",
          "ano": 1997
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Seção 1: Identificação dos Sintomas de TDAH",
          "descricao": "Questões para identificar sintomas de desatenção, hiperatividade e impulsividade.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Com que frequência o paciente tem dificuldades para manter a atenção em atividades de maneira contínua?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "moda_itens",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1.0,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2.0,
                  "ordem": 3
                },
                {
                  "texto": "Sempre",
                  "valor": 3.0,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O paciente comete erros por desatenção em atividades escolares ou tarefas do dia a dia?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente frequentemente parece não ouvir quando lhe falam diretamente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente tem dificuldades em seguir instruções ou concluir tarefas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente evita ou tem aversão a tarefas que exigem esforço mental sustentado (ex. leitura, fazer lição de casa)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente perde coisas frequentemente, como material escolar ou brinquedos?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente se movimenta constantemente ou não consegue ficar quieto em situações em que deveria?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente corre ou sobe em móveis de maneira excessiva ou inapropriada?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente tem dificuldades em permanecer sentado em situações como sala de aula ou refeições?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente fala excessivamente, interrompendo outras pessoas constantemente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente tem dificuldades para esperar a sua vez em situações sociais ou jogos?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 11,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente interrompe conversas ou atividades de outras pessoas de maneira imprópria?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 12,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 2: Comorbidades e Outros Transtornos Psiquiátricos",
          "descricao": "Questões para investigar sintomas de ansiedade, depressão e transtornos de comportamento.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "O paciente tem preocupações excessivas ou medo de coisas que podem não acontecer?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente se sente constantemente tenso, nervoso ou com medo em situações novas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente tem dificuldades em relaxar ou frequentemente sente-se sobrecarregado emocionalmente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente tem mostrado desinteresse por atividades que anteriormente eram prazerosas?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente parece estar triste, irritado ou com baixa energia a maior parte do tempo?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente tem problemas para dormir ou comer, ou faz isso excessivamente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente demonstra comportamentos agressivos ou desafiadores em relação à autoridade?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente tem episódios de explosões emocionais, como agressões físicas ou verbais?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente tem comportamentos destrutivos em casa ou na escola?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 3: Avaliação do Funcionamento Global e Impacto dos Sintomas",
          "descricao": "Questões para avaliar o impacto dos sintomas no funcionamento diário.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "Os sintomas de desatenção, hiperatividade e impulsividade interferem nas atividades diárias do paciente, como escola, atividades sociais e familiares?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Os sintomas são mais intensos em algum ambiente específico (escola, casa, outros)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "A família ou os professores reportam dificuldades significativas no comportamento ou desempenho do paciente?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "O paciente já foi diagnosticado com outro transtorno psiquiátrico no passado (ex. Transtorno de Ansiedade, Depressão, Transtorno de Conduta)?",
              "tipo_resposta": "booleano",
              "metodo_pontuacao": "moda_itens",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Escala de Avaliação de Comportamento de Achenbach (CBCL) para TDAH",
      "descricao": "Escala CBCL para avaliação de comportamentos de hiperatividade/impulsividade, desatenção e emocionais/sociais relacionados ao TDAH em crianças e adolescentes (6-18 anos).",
      "versao": "2.0",
      "fontes_literatura": [
        {
          "titulo": "Child Behavior Checklist for Ages 6-18 (CBCL/6-18)",
          "autores": "Achenbach, T. M., & Rescorla, L. A.",
          "ano": 2001
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Hiperatividade",
          "descricao": "Questões relacionadas à atividade motora excessiva.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "O indivíduo tem dificuldades para permanecer sentado ou tranquilo em situações onde se espera calma (por exemplo, durante aulas ou reuniões)? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo parece ter uma necessidade constante de se mover, como balançar as pernas, bater os pés ou mexer as mãos? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo sente a necessidade de se levantar e andar por todo o lugar, mesmo quando não há uma razão objetiva para isso? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele ou ela frequentemente se envolve em atividades excessivas e não controladas, como falar constantemente ou iniciar muitas tarefas sem terminá-las? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O comportamento motor excessivo (como correr ou pular) é mais intenso em situações onde o controle e a calma são exigidos? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "2. Impulsividade",
          "descricao": "Questões relacionadas à dificuldade em controlar respostas automáticas ou impulsivas.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "O indivíduo frequentemente interrompe outras pessoas durante uma conversa ou atividade, sem esperar sua vez? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele ou ela tem dificuldades para controlar respostas automáticas, como falar sem pensar ou agir impulsivamente? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo tem dificuldade em planejar ou organizar suas atividades, optando por soluções rápidas e impulsivas? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo frequentemente age sem considerar as consequências a longo prazo de suas ações? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo tende a ser impaciente, com dificuldade para esperar por sua vez ou para aguardar situações em que a ação não seja imediata? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "3. Comportamentos Disruptivos e Dificuldade de Planejamento",
          "descricao": "Questões relacionadas à dificuldade de organizar tarefas e manter o foco.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "O indivíduo tem dificuldade em iniciar ou concluir tarefas que exigem organização e planejamento? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele ou ela frequentemente perde prazos, compromissos ou tarefas importantes devido à falta de organização? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo toma decisões precipitadas e, muitas vezes, não consegue avaliar corretamente os riscos de suas ações? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo é incapaz de manter a calma ou controlar emoções em situações estressantes ou novas? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele ou ela frequentemente começa atividades, mas não consegue completá-las, abandonando-as no meio do caminho? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Escala de Hiperatividade e Impulsividade de Brown (Brown Attention Deficit Disorder Scales)",
      "descricao": "Escala para avaliar sintomas de hiperatividade e impulsividade em adolescentes e adultos (12+ anos).",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Brown Attention-Deficit Disorder Scales for Adolescents and Adults (BADDS)",
          "autores": "Brown, T. E.",
          "ano": 2001
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Hiperatividade",
          "descricao": "Questões relacionadas à atividade motora excessiva.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "O indivíduo tem dificuldades para permanecer sentado ou tranquilo em situações onde se espera calma (por exemplo, durante aulas ou reuniões)? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo parece ter uma necessidade constante de se mover, como balançar as pernas, bater os pés ou mexer as mãos? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo sente a necessidade de se levantar e andar por todo o lugar, mesmo quando não há uma razão objetiva para isso? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele ou ela frequentemente se envolve em atividades excessivas e não controladas, como falar constantemente ou iniciar muitas tarefas sem terminá-las? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O comportamento motor excessivo (como correr ou pular) é mais intenso em situações onde o controle e a calma são exigidos? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "2. Impulsividade",
          "descricao": "Questões relacionadas à dificuldade em controlar respostas automáticas ou impulsivas.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "O indivíduo frequentemente interrompe outras pessoas durante uma conversa ou atividade, sem esperar sua vez? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele ou ela tem dificuldades para controlar respostas automáticas, como falar sem pensar ou agir impulsivamente? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo tem dificuldade em planejar ou organizar suas atividades, optando por soluções rápidas e impulsivas? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo frequentemente age sem considerar as consequências a longo prazo de suas ações? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo tende a ser impaciente, com dificuldade para esperar por sua vez ou para aguardar situações em que a ação não seja imediata? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "3. Comportamentos Disruptivos e Dificuldade de Planejamento",
          "descricao": "Questões relacionadas à dificuldade de organizar tarefas e manter o foco.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "O indivíduo tem dificuldade em iniciar ou concluir tarefas que exigem organização e planejamento? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele ou ela frequentemente perde prazos, compromissos ou tarefas importantes devido à falta de organização? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo toma decisões precipitadas e, muitas vezes, não consegue avaliar corretamente os riscos de suas ações? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "O indivíduo é incapaz de manter a calma ou controlar emoções em situações estressantes ou novas? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Ele ou ela frequentemente começa atividades, mas não consegue completá-las, abandonando-as no meio do caminho? (Pontuação: 0 a 3)",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca ou raramente",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente ou sempre",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Investigação sobre o Histórico Familiar e Anamnese do TDAH",
      "descricao": "Questionário para investigar o histórico familiar, gestacional, de desenvolvimento e comportamental para avaliação do TDAH.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Manual de Diagnóstico e Estatístico de Transtornos Mentais (DSM-5)",
          "autores": "American Psychiatric Association",
          "ano": 2013
        },
        {
          "titulo": "Princípios de Neurociência",
          "autores": "Kandel, E. R., Schwartz, J. H., Jessell, T. M., Siegelbaum, S. A., & Hudspeth, A. J.",
          "ano": 2013
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Coleta de Dados Iniciais",
          "descricao": "Perguntas principais para o histórico familiar.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Existem casos de TDAH na família? Pai, mãe, irmãos, avós, tios, ou primos têm diagnóstico de TDAH ou apresentaram sintomas semelhantes?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Algum membro da família foi diagnosticado com transtornos comórbidos ao TDAH? Exemplos: Transtornos de ansiedade, depressão, transtorno de conduta, dificuldades de aprendizagem.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Existem outros distúrbios do desenvolvimento cognitivo ou comportamental na família? Dificuldades de aprendizagem, problemas de memória, habilidades de planejamento, problemas com impulsividade.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "2. História da Gravidez e Nascimento",
          "descricao": "Perguntas relevantes sobre a gestação, parto e período neonatal.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "A gestação foi saudável? Houve complicações como infecções, hipertensão ou uso de substâncias durante a gravidez?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "O parto foi normal ou houve complicações? Parto prematuro, dificuldades de oxigenação, uso de fórceps, cesariana de emergência?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Houve problemas no período neonatal? Baixo peso ao nascer, icterícia, hospitalização prolongada ou necessidade de cuidados especiais?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "3. Anamnese do Desenvolvimento Infantil",
          "descricao": "Perguntas para entender o desenvolvimento da criança em termos de linguagem, habilidades motoras, sociais e acadêmicas.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "Quando a criança começou a andar e falar? Há atrasos no desenvolvimento motor ou de linguagem? Quais marcos de desenvolvimento foram atrasados?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Quais foram os primeiros sinais de dificuldade de atenção ou comportamento? A criança apresentou dificuldades para se concentrar em atividades desde a primeira infância? Como os pais perceberam essas dificuldades?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Como a criança se comportava em casa, na escola e em interações sociais? Comportamento impulsivo, dificuldades para seguir instruções, hiperatividade ou comportamento desafiador?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "A criança teve dificuldades acadêmicas? Quais matérias foram mais difíceis? A criança teve problemas com organização, planejamento ou cumprimento de tarefas escolares?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 4,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "4. Investigação sobre o Comportamento Atual",
          "descricao": "Perguntas para entender como o paciente lida com suas tarefas diárias.",
          "ordem": 4,
          "perguntas": [
            {
              "texto": "Quais são as dificuldades atuais no ambiente escolar/trabalho? Dificuldade para manter o foco, concluir tarefas ou seguir instruções? A pessoa precisa de mais tempo para completar atividades?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Como a pessoa lida com responsabilidades cotidianas? A pessoa se sente desorganizada, desatenta ou impulsiva nas atividades diárias? Há histórico de dificuldades em gerenciar tempo e prioridades?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Há problemas com comportamentos impulsivos ou hiperatividade? A pessoa interrompe os outros, tem dificuldades para aguardar a vez ou apresenta inquietação excessiva?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Qual o impacto desses sintomas nas relações sociais e familiares? Existe um histórico de conflitos familiares ou sociais devido ao comportamento impulsivo ou desatento? Como o paciente interage com amigos e familiares?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 4,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "5. Investigar a Comorbidade com Outras Condições Psiquiátricas",
          "descricao": "Perguntas sobre a presença de comorbidades associadas ao TDAH.",
          "ordem": 5,
          "perguntas": [
            {
              "texto": "Algum membro da família tem diagnóstico de transtornos de ansiedade, depressão ou distúrbios de humor?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Existem sinais de depressão, ansiedade ou problemas emocionais na criança/adolescente/adulto? Como a pessoa lida com o estresse ou frustração? Há dificuldades com o controle emocional?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Há alguma dificuldade significativa em habilidades acadêmicas ou sociais que possa indicar um transtorno de aprendizado?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "6. Questionário Genético e Ambiental",
          "descricao": "Perguntas sobre histórico familiar de saúde mental e fatores ambientais de risco.",
          "ordem": 6,
          "perguntas": [
            {
              "texto": "Há histórico familiar de doenças psiquiátricas ou neurológicas? Transtornos de ansiedade, depressão, esquizofrenia, epilepsia, entre outros.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "A família tem antecedentes de problemas de abuso de substâncias, alcoolismo ou comportamento criminal? Fatores ambientais de risco podem contribuir para a manifestação de sintomas de TDAH.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Quais fatores ambientais podem estar influenciando a criança/adolescente/adulto? Mudanças significativas no ambiente (divórcio dos pais, mudança de escola, trauma) podem desencadear ou exacerbar os sintomas.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        }
      ]
    },
    {
      "titulo": "Teste de Avaliação de TDAH - Escala de Conners para Crianças e Pais Responsáveis",
      "descricao": "Escala de Conners para rastreamento de TDAH em crianças de 6 a 12 anos.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Conners' Rating Scales",
          "autores": "Conners, C. K.",
          "ano": 1997
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Atenção e Concentração",
          "descricao": "Questões relacionadas à atenção e concentração.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Distrai-se facilmente com ruídos ou estímulos ao redor.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em manter o foco em atividades escolares ou tarefas em casa.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Frequentemente começa uma tarefa e logo a abandona sem terminar.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Esquece com frequência o que foi pedido para fazer.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Parece não ouvir quando falam diretamente com ele/ela.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "2. Hiperatividade e Impulsividade",
          "descricao": "Questões relacionadas à hiperatividade e impulsividade.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Mexe-se constantemente, balança mãos ou pés quando está sentado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Corre ou sobe em móveis de forma inadequada, mesmo em ambientes que não permitem isso.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Tem dificuldade em esperar a sua vez em brincadeiras ou conversas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Fala excessivamente, sem parar.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "Interrompe ou se intromete nas conversas e atividades dos outros.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Ocasionalmente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Investigação sobre o Histórico Familiar e Anamnese do TDAH",
      "descricao": "Questionário para investigar o histórico familiar, gestacional, de desenvolvimento e comportamental para avaliação do TDAH.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Manual de Diagnóstico e Estatístico de Transtornos Mentais (DSM-5)",
          "autores": "American Psychiatric Association",
          "ano": 2013
        },
        {
          "titulo": "Princípios de Neurociência",
          "autores": "Kandel, E. R., Schwartz, J. H., Jessell, T. M., Siegelbaum, S. A., & Hudspeth, A. J.",
          "ano": 2013
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Coleta de Dados Iniciais",
          "descricao": "Perguntas principais para o histórico familiar.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Existem casos de TDAH na família? Pai, mãe, irmãos, avós, tios, ou primos têm diagnóstico de TDAH ou apresentaram sintomas semelhantes?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Algum membro da família foi diagnosticado com transtornos comórbidos ao TDAH? Exemplos: Transtornos de ansiedade, depressão, transtorno de conduta, dificuldades de aprendizagem.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Existem outros distúrbios do desenvolvimento cognitivo ou comportamental na família? Dificuldades de aprendizagem, problemas de memória, habilidades de planejamento, problemas com impulsividade.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "2. História da Gravidez e Nascimento",
          "descricao": "Perguntas relevantes sobre a gestação, parto e período neonatal.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "A gestação foi saudável? Houve complicações como infecções, hipertensão ou uso de substâncias durante a gravidez?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "O parto foi normal ou houve complicações? Parto prematuro, dificuldades de oxigenação, uso de fórceps, cesariana de emergência?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Houve problemas no período neonatal? Baixo peso ao nascer, icterícia, hospitalização prolongada ou necessidade de cuidados especiais?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "3. Anamnese do Desenvolvimento Infantil",
          "descricao": "Perguntas para entender o desenvolvimento da criança em termos de linguagem, habilidades motoras, sociais e acadêmicas.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "Quando a criança começou a andar e falar? Há atrasos no desenvolvimento motor ou de linguagem? Quais marcos de desenvolvimento foram atrasados?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Quais foram os primeiros sinais de dificuldade de atenção ou comportamento? A criança apresentou dificuldades para se concentrar em atividades desde a primeira infância? Como os pais perceberam essas dificuldades?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Como a criança se comportava em casa, na escola e em interações sociais? Comportamento impulsivo, dificuldades para seguir instruções, hiperatividade ou comportamento desafiador?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "A criança teve dificuldades acadêmicas? Quais matérias foram mais difíceis? A criança teve problemas com organização, planejamento ou cumprimento de tarefas escolares?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 4,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "4. Investigação sobre o Comportamento Atual",
          "descricao": "Perguntas para entender como o paciente lida com suas tarefas diárias.",
          "ordem": 4,
          "perguntas": [
            {
              "texto": "Quais são as dificuldades atuais no ambiente escolar/trabalho? Dificuldade para manter o foco, concluir tarefas ou seguir instruções? A pessoa precisa de mais tempo para completar atividades?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Como a pessoa lida com responsabilidades cotidianas? A pessoa se sente desorganizada, desatenta ou impulsiva nas atividades diárias? Há histórico de dificuldades em gerenciar tempo e prioridades?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Há problemas com comportamentos impulsivos ou hiperatividade? A pessoa interrompe os outros, tem dificuldades para aguardar a vez ou apresenta inquietação excessiva?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Qual o impacto desses sintomas nas relações sociais e familiares? Existe um histórico de conflitos familiares ou sociais devido ao comportamento impulsivo ou desatento? Como o paciente interage com amigos e familiares?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 4,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "5. Investigar a Comorbidade com Outras Condições Psiquiátricas",
          "descricao": "Perguntas sobre a presença de comorbidades associadas ao TDAH.",
          "ordem": 5,
          "perguntas": [
            {
              "texto": "Algum membro da família tem diagnóstico de transtornos de ansiedade, depressão ou distúrbios de humor?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Existem sinais de depressão, ansiedade ou problemas emocionais na criança/adolescente/adulto? Como a pessoa lida com o estresse ou frustração? Há dificuldades com o controle emocional?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Há alguma dificuldade significativa em habilidades acadêmicas ou sociais que possa indicar um transtorno de aprendizado?",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "6. Questionário Genético e Ambiental",
          "descricao": "Perguntas sobre histórico familiar de saúde mental e fatores ambientais de risco.",
          "ordem": 6,
          "perguntas": [
            {
              "texto": "Há histórico familiar de doenças psiquiátricas ou neurológicas? Transtornos de ansiedade, depressão, esquizofrenia, epilepsia, entre outros.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 1,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "A família tem antecedentes de problemas de abuso de substâncias, alcoolismo ou comportamento criminal? Fatores ambientais de risco podem contribuir para a manifestação de sintomas de TDAH.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 2,
              "is_obrigatoria": False,
              "alternativas": []
            },
            {
              "texto": "Quais fatores ambientais podem estar influenciando a criança/adolescente/adulto? Mudanças significativas no ambiente (divórcio dos pais, mudança de escola, trauma) podem desencadear ou exacerbar os sintomas.",
              "tipo_resposta": "texto_livre",
              "metodo_pontuacao": "qualitativo",
              "ordem": 3,
              "is_obrigatoria": False,
              "alternativas": []
            }
          ]
        }
      ]
    },
    {
      "titulo": "Teste de Avaliação de TDAH – Escala de Conners para Adolescentes (13 a 17 anos)",
      "descricao": "Escala de Conners para rastreamento de TDAH em adolescentes de 13 a 17 anos, considerando dificuldades acadêmicas, emocionais e sociais, com base na Escala de Conners e no DSM-5.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Conners' Rating Scales",
          "autores": "Conners, C. K.",
          "ano": 1997
        },
        {
          "titulo": "Manual de Diagnóstico e Estatístico de Transtornos Mentais (DSM-5)",
          "autores": "American Psychiatric Association",
          "ano": 2013
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Seção 1: Déficit de Atenção (Inatenção)",
          "descricao": None,
          "ordem": 1,
          "perguntas": [
            {
              "texto": "1️⃣ Distrai-se facilmente com estímulos externos (celular, barulhos, conversas, redes sociais).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Tem dificuldade em manter a atenção em aulas, leituras longas ou tarefas demoradas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Comete erros por descuido em provas, trabalhos e atividades acadêmicas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Parece não ouvir quando alguém fala diretamente com ele/ela.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Esquece frequentemente prazos, compromissos ou materiais escolares.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Tem dificuldade para se organizar e planejar atividades (exemplo: estudar para provas).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Perde frequentemente objetos importantes (celular, carteira, fones, cadernos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Evita ou procrastina tarefas que exigem esforço mental prolongado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Tem dificuldades para seguir instruções detalhadas ou executar tarefas por etapas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Alterna entre várias atividades sem completar nenhuma adequadamente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 2: Hiperatividade e Impulsividade",
          "descricao": None,
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Sente-se inquieto(a) e tem dificuldade em permanecer sentado(a) por longos períodos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Fala excessivamente, às vezes interrompendo outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Interrompe conversas e atividades alheias sem perceber.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Age impulsivamente sem pensar nas consequências (como enviar mensagens sem refletir).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Tem dificuldade em esperar sua vez em discussões ou atividades em grupo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Responde perguntas antes de serem concluídas, sem pensar na resposta.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Tem uma necessidade constante de estar se movimentando (batucando, balançando pernas).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Busca estímulos frequentes, podendo recorrer a comportamentos de risco (como direção perigosa).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Apresenta explosões emocionais repentinas e dificuldade para controlar frustrações.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Age sem avaliar os riscos, como gastar dinheiro sem planejamento ou aceitar desafios imprudentes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 3: Impacto Acadêmico, Social e Emocional",
          "descricao": None,
          "ordem": 3,
          "perguntas": [
            {
              "texto": "1️⃣ Tem dificuldades para manter amizades devido à impulsividade ou distração.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Apresenta baixo desempenho escolar apesar de ter capacidade intelectual adequada.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Esquece frequentemente compromissos ou chega atrasado(a) a eventos e aulas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Professores relatam desatenção, inquietação ou falta de comprometimento nas aulas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Sente-se frustrado(a) por não conseguir cumprir prazos ou manter a organização.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Enfrenta dificuldades para regular emoções, ficando irritado(a) ou frustrado(a) facilmente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Sente-se ansioso(a) ou sobrecarregado(a) por não conseguir administrar tarefas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Relata baixa autoestima ou sensação de incapacidade por não atingir expectativas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Tem dificuldade para manter o foco em atividades de longo prazo, como estudar para vestibulares.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Busca estímulos constantes para evitar o tédio, podendo negligenciar obrigações.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Teste de Avaliação de TDAH – Escala de Conners para Adolescentes (13 a 17 anos)",
      "descricao": "Escala de Conners para rastreamento de TDAH em adolescentes de 13 a 17 anos, considerando dificuldades acadêmicas, emocionais e sociais, com base na Escala de Conners e no DSM-5.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Conners' Rating Scales",
          "autores": "Conners, C. K.",
          "ano": 1997
        },
        {
          "titulo": "Manual de Diagnóstico e Estatístico de Transtornos Mentais (DSM-5)",
          "autores": "American Psychiatric Association",
          "ano": 2013
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Seção 1: Déficit de Atenção (Inatenção)",
          "descricao": None,
          "ordem": 1,
          "perguntas": [
            {
              "texto": "1️⃣ Distrai-se facilmente com estímulos externos (celular, barulhos, conversas, redes sociais).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Tem dificuldade em manter a atenção em aulas, leituras longas ou tarefas demoradas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Comete erros por descuido em provas, trabalhos e atividades acadêmicas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Parece não ouvir quando alguém fala diretamente com ele/ela.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Esquece frequentemente prazos, compromissos ou materiais escolares.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Tem dificuldade para se organizar e planejar atividades (exemplo: estudar para provas).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Perde frequentemente objetos importantes (celular, carteira, fones, cadernos).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Evita ou procrastina tarefas que exigem esforço mental prolongado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Tem dificuldades para seguir instruções detalhadas ou executar tarefas por etapas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Alterna entre várias atividades sem completar nenhuma adequadamente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 2: Hiperatividade e Impulsividade",
          "descricao": None,
          "ordem": 2,
          "perguntas": [
            {
              "texto": "1️⃣ Sente-se inquieto(a) e tem dificuldade em permanecer sentado(a) por longos períodos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Fala excessivamente, às vezes interrompendo outras pessoas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Interrompe conversas e atividades alheias sem perceber.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Age impulsivamente sem pensar nas consequências (como enviar mensagens sem refletir).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Tem dificuldade em esperar sua vez em discussões ou atividades em grupo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Responde perguntas antes de serem concluídas, sem pensar na resposta.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Tem uma necessidade constante de estar se movimentando (batucando, balançando pernas).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Busca estímulos frequentes, podendo recorrer a comportamentos de risco (como direção perigosa).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Apresenta explosões emocionais repentinas e dificuldade para controlar frustrações.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Age sem avaliar os riscos, como gastar dinheiro sem planejamento ou aceitar desafios imprudentes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 3: Impacto Acadêmico, Social e Emocional",
          "descricao": None,
          "ordem": 3,
          "perguntas": [
            {
              "texto": "1️⃣ Tem dificuldades para manter amizades devido à impulsividade ou distração.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Apresenta baixo desempenho escolar apesar de ter capacidade intelectual adequada.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Esquece frequentemente compromissos ou chega atrasado(a) a eventos e aulas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Professores relatam desatenção, inquietação ou falta de comprometimento nas aulas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Sente-se frustrado(a) por não conseguir cumprir prazos ou manter a organização.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Enfrenta dificuldades para regular emoções, ficando irritado(a) ou frustrado(a) facilmente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Sente-se ansioso(a) ou sobrecarregado(a) por não conseguir administrar tarefas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Relata baixa autoestima ou sensação de incapacidade por não atingir expectativas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Tem dificuldade para manter o foco em atividades de longo prazo, como estudar para vestibulares.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Busca estímulos constantes para evitar o tédio, podendo negligenciar obrigações.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Teste de Avaliação de TDAH – Escala de Conners para Adultos",
      "descricao": "Avaliação completa e aprofundada baseada na Escala de Conners para TDAH em adultos, com categorias bem definidas, interpretação detalhada e pontuação rigorosa.\n\n**Objetivo:** Este teste ajuda a identificar sinais de TDAH em adultos, com base em critérios científicos utilizados na Escala de Conners e no DSM-5.\n\n**Instruções:** Leia atentamente cada afirmação e marque a opção que melhor descreve sua experiência nas últimas 4 semanas.\n\n**Frequência do Comportamento e Pontuação:**\n- Nunca (0% das vezes): 0 pontos\n- Raramente (25% das vezes): 1 ponto\n- Frequentemente (50% das vezes): 2 pontos\n- Muito frequentemente (75% ou mais): 3 pontos\n\n**Interpretação dos Resultados:**\n**Pontuação Total:** Some os pontos das três seções.\n- 0 - 20 pontos: Dentro da normalidade (Não há sinais significativos de TDAH. O comportamento está dentro do esperado para a idade.)\n- 21 - 40 pontos: Leve (Alguns sintomas de desatenção e hiperatividade. Monitoramento recomendado.)\n- 41 - 60 pontos: Moderado (Indícios consistentes de TDAH. Avaliação profissional sugerida.)\n- 61 - 90 pontos: Severo (Alta probabilidade de TDAH. Importante procurar um especialista para diagnóstico detalhado.)\n\n**Análise Clínica e Considerações:**\n- **Déficit de Atenção Predominante:** Se a pontuação for maior na Seção 1, há indícios de TDAH do Tipo Desatento, caracterizado por dificuldades de foco, esquecimento e desorganização.\n- **Hiperatividade/Impulsividade Predominante:** Se a pontuação for maior na Seção 2, há indícios de TDAH do Tipo Hiperativo-Impulsivo, marcado por inquietação, impulsividade e dificuldades em controlar ações e emoções.\n- **TDAH Combinado:** Se a pontuação for alta em ambas as seções (1 e 2), há sinais de TDAH do Tipo Combinado, que envolve sintomas significativos de desatenção e hiperatividade.\n- **Impacto Funcional:** Uma pontuação alta na Seção 3 sugere que os sintomas estão afetando negativamente a vida profissional, social e emocional, reforçando a necessidade de uma avaliação especializada.\n\n**Próximos Passos:** Se sua pontuação indica moderado ou severo, recomenda-se:\n- Consulta com especialista (psiquiatra, neuropsicólogo ou neurologista).\n- Entrevista clínica detalhada sobre histórico de sintomas desde a infância.\n- Testes neuropsicológicos complementares, se necessário.\n- Abordagem terapêutica, que pode incluir psicoterapia, coaching para TDAH e, em alguns casos, medicação.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Conners' Rating Scales",
          "autores": "Conners, C. K.",
          "ano": 1997
        },
        {
          "titulo": "Manual de Diagnóstico e Estatístico de Transtornos Mentais (DSM-5)",
          "autores": "American Psychiatric Association",
          "ano": 2013
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Seção 1: Déficit de Atenção",
          "descricao": None,
          "ordem": 1,
          "perguntas": [
            {
              "texto": "1️⃣ Tenho dificuldade em manter o foco em tarefas ou atividades prolongadas (exemplo: trabalho, leitura, estudo).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Distrai-me facilmente com sons, estímulos visuais ou pensamentos internos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Esqueço de compromissos, prazos ou obrigações importantes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Tenho dificuldades em organizar tarefas e materiais necessários para atividades do dia a dia.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Deixo tarefas inacabadas porque perco o interesse ou foco rapidamente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Tenho dificuldades para seguir instruções detalhadas ou realizar tarefas que exigem várias etapas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Perco frequentemente objetos essenciais (chaves, carteira, celular, documentos, etc.).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Tenho dificuldade em escutar atentamente quando alguém fala comigo, mesmo que seja um assunto importante.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Evito ou adio tarefas que exigem esforço mental contínuo (como planejamento financeiro, relatórios, leituras longas).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Alterno rapidamente entre uma atividade e outra sem completar nenhuma.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 2: Hiperatividade e Impulsividade",
          "descricao": None,
          "ordem": 2,
          "perguntas": [
            {
              "texto": "1️⃣ Sinto-me inquieto(a) e tenho dificuldade em ficar parado(a) por longos períodos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Mexo constantemente as mãos, pés ou me movimento excessivamente quando deveria estar tranquilo(a).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Tenho dificuldade em permanecer sentado(a) em reuniões, palestras ou eventos prolongados.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Sinto uma necessidade intensa de estar sempre ocupado(a) ou envolvido(a) em alguma atividade.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Falo excessivamente, muitas vezes sem perceber que estou interrompendo os outros.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Tenho dificuldade em esperar minha vez em filas, reuniões ou conversas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Frequentemente termino frases das outras pessoas ou dou respostas antes que a pergunta seja concluída.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Interrompo ou me intrometo em conversas e atividades de outras pessoas, sem perceber que isso pode ser inadequado.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Tomo decisões impulsivas sem considerar as consequências, o que pode gerar problemas financeiros, profissionais ou sociais.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Muitas vezes sinto a necessidade de estar sempre em movimento, como se tivesse um \"motor ligado\".",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 3: Impacto na Vida Pessoal e Profissional",
          "descricao": None,
          "ordem": 3,
          "perguntas": [
            {
              "texto": "1️⃣ Tenho dificuldades em manter a organização no ambiente de trabalho ou em casa.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Sofro com atrasos frequentes devido à má gestão do tempo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Esqueço de responder e-mails, mensagens ou retornar ligações importantes.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Tenho dificuldades em manter relacionamentos devido à impulsividade ou esquecimento.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Minha produtividade no trabalho ou estudo é prejudicada por dificuldades de foco e organização.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Sinto-me sobrecarregado(a) com tarefas simples porque procrastino ou me desorganizo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Frequentemente mudo de interesses ou metas antes de concluí-los.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Tenho dificuldade em controlar emoções, como frustração ou irritabilidade.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Sofro com sentimentos de baixa autoestima ou frustração por não conseguir atingir meu potencial.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Já fui criticado(a) por outros devido à minha desatenção, impulsividade ou dificuldade de organização.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Teste de Avaliação de TDAH – Escala de Conners para Crianças 6 a 12 anos",
      "descricao": "Teste aprofundado baseado na Escala de Conners para Crianças, uma ferramenta cientificamente validada para rastrear o Transtorno do Déficit de Atenção e Hiperatividade (TDAH). O teste inclui categorias bem definidas, pontuação rigorosa e interpretação detalhada dos resultados.\n\n**Faixa Etária:** 6 a 12 anos\n\n**Objetivo:** Este teste auxilia pais, responsáveis e profissionais da educação a identificar possíveis sinais de TDAH em crianças, de acordo com critérios científicos da Escala de Conners e do DSM-5.\n\n**Instruções:** Os pais, responsáveis ou professores devem avaliar o comportamento da criança nos últimos 6 meses e marcar a opção que melhor descreve a frequência de cada comportamento.\n\n**Frequência do Comportamento e Pontuação:**\n- Nunca (0% das vezes): 0 pontos\n- Raramente (25% das vezes): 1 ponto\n- Frequentemente (50% das vezes): 2 pontos\n- Muito frequentemente (75% ou mais): 3 pontos\n\n**Interpretação dos Resultados:**\n**Pontuação Total:** Some os pontos das três seções.\n- 0 - 20 pontos: Dentro da normalidade (O comportamento está dentro do esperado para a idade.)\n- 21 - 40 pontos: Leve (Alguns sintomas de desatenção e hiperatividade. Monitoramento recomendado.)\n- 41 - 60 pontos: Moderado (Indícios consistentes de TDAH. Avaliação profissional sugerida.)\n- 61 - 90 pontos: Severo (Alta probabilidade de TDAH. Importante procurar um especialista para diagnóstico detalhado.)\n\n**Análise Clínica e Considerações:**\n- **Déficit de Atenção Predominante:** Se a pontuação for maior na Seção 1, há indícios de TDAH do Tipo Desatento, caracterizado por dificuldades de foco, esquecimento e desorganização.\n- **Hiperatividade/Impulsividade Predominante:** Se a pontuação for maior na Seção 2, há indícios de TDAH do Tipo Hiperativo-Impulsivo, marcado por inquietação, impulsividade e dificuldades em controlar ações e emoções.\n- **TDAH Combinado:** Se a pontuação for alta em ambas as seções (1 e 2), há sinais de TDAH do Tipo Combinado, que envolve sintomas significativos de desatenção e hiperatividade.\n- **Impacto Funcional:** Uma pontuação alta na Seção 3 sugere que os sintomas estão afetando negativamente o desempenho escolar, social e emocional da criança, reforçando a necessidade de uma avaliação especializada.\n\n**Próximos Passos:** Se a pontuação da criança indica moderado ou severo, recomenda-se:\n- Consulta com especialista (neuropediatra, psiquiatra infantil ou psicólogo especializado).\n- Coleta de informações adicionais de professores e cuidadores sobre o comportamento da criança.\n- Testes neuropsicológicos complementares, se necessário.\n- Estratégias de manejo comportamental e suporte escolar para auxiliar na adaptação da criança.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Conners' Rating Scales",
          "autores": "Conners, C. K.",
          "ano": 1997
        },
        {
          "titulo": "Manual de Diagnóstico e Estatístico de Transtornos Mentais (DSM-5)",
          "autores": "American Psychiatric Association",
          "ano": 2013
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "Seção 1: Déficit de Atenção",
          "descricao": "(Inatenção)",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "1️⃣ Distrai-se facilmente com estímulos ao redor, como ruídos ou movimentos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Tem dificuldade em manter o foco em tarefas escolares ou brincadeiras estruturadas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Parece não ouvir quando falam diretamente com ele/ela.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Esquece frequentemente de realizar tarefas diárias, mesmo quando lembrado(a).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Tem dificuldade para organizar materiais e atividades escolares.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Evita ou adia atividades que exigem esforço mental contínuo (como lição de casa ou leitura).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Perde frequentemente objetos importantes, como cadernos, brinquedos ou material escolar.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Alterna rapidamente entre uma atividade e outra, sem completar nenhuma.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Tem dificuldade em seguir instruções, especialmente as que envolvem várias etapas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Parece estar sempre \"no mundo da lua\", mesmo quando deveria prestar atenção.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 2: Hiperatividade e Impulsividade",
          "descricao": None,
          "ordem": 2,
          "perguntas": [
            {
              "texto": "1️⃣ Mexe-se constantemente, balança mãos ou pés ou não consegue ficar parado(a).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ Levanta-se da cadeira em momentos inadequados (aula, refeições, etc.).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Corre ou escala móveis de forma inadequada, mesmo quando não é permitido.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Tem dificuldade em brincar ou se envolver em atividades de forma tranquila.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Está sempre inquieto(a), como se tivesse \"um motor ligado\".",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Fala excessivamente e de forma ininterrupta.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Responde perguntas antes de serem concluídas, sem esperar sua vez.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Tem dificuldade em esperar sua vez em jogos, conversas ou atividades em grupo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Interrompe conversas e atividades dos outros, se intrometendo sem perceber.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Age impulsivamente, sem considerar as consequências (exemplo: atravessar a rua sem olhar).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        },
        {
          "titulo": "Seção 3: Impacto Social e Escolar",
          "descricao": None,
          "ordem": 3,
          "perguntas": [
            {
              "texto": "1️⃣ Tem dificuldades para manter amizades devido ao comportamento impulsivo.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "2️⃣ É frequentemente repreendido(a) por professores devido à desatenção ou hiperatividade.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "3️⃣ Tem dificuldade para seguir regras ou respeitar limites impostos por adultos.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "4️⃣ Apresenta problemas de comportamento em mais de um ambiente (escola, casa, atividades sociais).",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "5️⃣ Sente-se frustrado(a) por não conseguir completar tarefas ou ser repreendido(a) frequentemente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "6️⃣ Necessita de mais supervisão do que outras crianças da mesma idade.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 6,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "7️⃣ Demonstra baixa tolerância à frustração, reagindo com irritação ou choro frequente.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 7,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "8️⃣ Tem dificuldades para entender e respeitar normas sociais.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 8,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "9️⃣ Apresenta comportamento desafiador ou oposição a figuras de autoridade.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 9,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            },
            {
              "texto": "🔟 Tem baixa autoestima ou sente-se desmotivado(a) por dificuldades acadêmicas.",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 10,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Nunca",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Raramente",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Frequentemente",
                  "valor": 2,
                  "ordem": 3
                },
                {
                  "texto": "Muito frequentemente",
                  "valor": 3,
                  "ordem": 4
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Escala Avaliativa para Avaliação de TDAH usando o Teste de Atenção Visual (IVA)",
      "descricao": "O Teste de Atenção Visual (IVA) é uma avaliação neuropsicológica amplamente utilizada para investigar o desempenho em tarefas de atenção, um dos domínios mais afetados pelo Transtorno de Déficit de Atenção e Hiperatividade (TDAH). O IVA é uma ferramenta que mede o desempenho da atenção sustentada, a capacidade de controle da atenção e o foco visual, aspectos frequentemente prejudicados em indivíduos com TDAH.\n\n**Faixa Etária:** O Teste de Atenção Visual (IVA) pode ser aplicado a indivíduos a partir de 6 anos de idade, sendo especialmente eficaz para crianças e adolescentes, mas também utilizado em adultos para avaliar o impacto do TDAH nas funções atencionais.\n\n**Objetivo da Avaliação:** O IVA tem como objetivo medir a atenção visual sustentada e a capacidade de resposta a estímulos visuais, avaliando as funções atencionais em dois eixos principais: Atenção Sustentada e Impulsividade. Além disso, o teste avalia o tempo de reação, a quantidade de respostas corretas e incorretas, e a variabilidade da atenção ao longo do tempo.\n\n**Estrutura do Teste:** O IVA consiste em uma série de tarefas que envolvem a observação e resposta a estímulos visuais. O participante deve responder a uma sequência de estímulos apresentados em tela, identificando e reagindo de acordo com as instruções fornecidas (geralmente, pressionar uma tecla quando um estímulo específico aparece). As principais variáveis avaliadas são: Tempo de reação, Taxa de erro e Variação de atenção.\n\n**Pontuação e Classificação:** Cada questão será pontuada de acordo com a frequência e a intensidade do comportamento observado: 0 = Comportamento nunca ou raramente observado, 1 = Comportamento ocasionalmente observado, 2 = Comportamento frequentemente observado. A pontuação total será a soma das respostas, com a interpretação da pontuação a seguir: Normal (0-20 pontos), Leve (21-40 pontos), Moderado (41-60 pontos), Grave (61+ pontos).\n\n**Interpretação dos Resultados:** Baixa Pontuação (0-20 pontos): Desempenho atencional dentro da faixa esperada. Pontuação Moderada (21-40 pontos): Apresenta algumas dificuldades em sustentar a atenção e evitar respostas impulsivas, sugerindo sintomas leves de TDAH. Pontuação Alta (41-60 pontos): Dificuldades atencionais moderadas a severas, com desafios significativos em manter o foco e controlar impulsos. Pontuação Muito Alta (61+ pontos): Desempenho significativamente comprometido, indicando possível quadro de TDAH.\n\n**Conclusão:** O Teste de Atenção Visual (IVA) é uma ferramenta eficaz para avaliar a capacidade de atenção em indivíduos com suspeita de TDAH.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Teste de Atenção Visual (IVA)",
          "autores": "IVA Research Foundation",
          "ano": None
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Atenção Sustentada",
          "descricao": None,
          "ordem": 1,
          "perguntas": [
            {
              "texto": "O participante demonstra uma capacidade consistente de manter o foco durante o teste, mesmo em tarefas repetitivas?",
              "tipo_resposta": "escala_likert_4",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Existe uma tendência a perder o foco após períodos curtos de tempo?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "A pessoa comete erros de distração ou falha em perceber estímulos devido à perda de atenção durante o teste?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O tempo de resposta do participante se mantém dentro dos parâmetros esperados ao longo do teste, ou há flutuações evidentes?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante consegue sustentar a atenção por todo o tempo da tarefa, ou demonstra lapsos de concentração?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            }
          ]
        },
        {
          "titulo": "2. Impulsividade e Controle de Respostas",
          "descricao": None,
          "ordem": 2,
          "perguntas": [
            {
              "texto": "O indivíduo responde de forma impulsiva, sem esperar a instrução completa ou sem processar corretamente o estímulo?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "A pessoa tem dificuldade em inibir respostas automáticas, cometendo erros frequentes de impulsividade?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante comete respostas rápidas sem verificar corretamente o estímulo visual?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Existe uma tendência a interromper a tarefa ou agir impulsivamente sem seguir o procedimento?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante consegue regular suas respostas de maneira eficiente, ou os erros de impulsividade são predominantes?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            }
          ]
        },
        {
          "titulo": "3. Variabilidade da Atenção",
          "descricao": None,
          "ordem": 3,
          "perguntas": [
            {
              "texto": "O desempenho do participante é consistente ao longo de todo o teste, ou há variação significativa nas respostas?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante mostra sinais de fadiga ou perda de atenção conforme o teste progride?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O tempo de resposta se altera de forma irregular, indicando dificuldade de manter a atenção estável?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante apresenta períodos em que sua atenção flutua consideravelmente, perdendo o foco e apresentando erros mais frequentes?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "A pessoa parece ter facilidade em manter o foco durante os estímulos repetidos, ou frequentemente perde a concentração?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            }
          ]
        },
        {
          "titulo": "4. Eficiência e Tempo de Resposta",
          "descricao": None,
          "ordem": 4,
          "perguntas": [
            {
              "texto": "O tempo de reação do participante é geralmente mais lento do que o esperado?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante demora a responder a estímulos, sugerindo dificuldade em manter a atenção visual constante?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Existe uma correlação entre a demora na resposta e erros frequentes de atenção?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante é eficiente em seu desempenho, com tempos de resposta rápidos e precisos?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O indivíduo se adapta de forma eficiente a mudanças no teste, ou tem dificuldades para ajustar a atenção?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Escala Avaliativa para TDAH usando o Wisconsin Card Sorting Test (WCST)",
      "descricao": "O Wisconsin Card Sorting Test (WCST) é uma avaliação neuropsicológica altamente reconhecida, que tem sido usada de forma eficaz para investigar funções executivas, como flexibilidade cognitiva, tomada de decisão, atenção e capacidade de adaptação. Embora seja tradicionalmente usada para estudar disfunções cerebrais e transtornos neuropsiquiátricos, o WCST também é útil na avaliação do TDAH, especialmente para investigar deficiências em controle cognitivo, impulsividade, e atenção.\n\nO WCST testa a capacidade de mudar de estratégia de acordo com feedback ambiental, o que é um componente crucial para indivíduos com TDAH, que frequentemente apresentam dificuldades em manter ou ajustar estratégias para lidar com novas informações ou desafios.\n\n**Faixa Etária:** O WCST é geralmente aplicado a indivíduos a partir de 6 anos de idade, sendo mais amplamente utilizado em adolescentes e adultos. No entanto, seu uso é frequentemente feito com pessoas acima de 10 anos devido à complexidade das tarefas e necessidade de compreensão do feedback de classificação.\n\n**Objetivo da Avaliação:** O WCST é projetado para avaliar funções executivas e processos cognitivos, como: Flexibilidade cognitiva, Planejamento e tomada de decisão, Monitoramento e controle da atenção. Este teste pode ajudar a identificar as dificuldades cognitivas associadas ao TDAH, como a incapacidade de ajustar estratégias e responder de forma adaptativa a mudanças.\n\n**Estrutura do WCST:** O WCST consiste em uma série de cartões coloridos, que o indivíduo deve classificar de acordo com um critério que é alterado aleatoriamente, e o participante deve se adaptar a essa mudança sem ser informado. O teste pode ser realizado manualmente ou usando uma versão computadorizada.\n\n**Pontuação e Classificação:** Cada uma das questões será pontuada com base na frequência ou intensidade dos comportamentos observados: 0 = Comportamento nunca ou raramente observado, 1 = Comportamento ocasionalmente observado, 2 = Comportamento frequentemente observado. A pontuação total será a soma dos itens, com a interpretação da pontuação da seguinte maneira: Normal (0-16 pontos), Leve (17-32 pontos), Moderado (33-48 pontos), Grave (49+ pontos).\n\n**Interpretação dos Resultados:** Baixa Pontuação (0-16 pontos): Boa habilidade para se adaptar a mudanças de estratégia e controle cognitivo. Pontuação Moderada (17-32 pontos): Dificuldades leves a moderadas em flexibilidade cognitiva e controle de impulsos, indicativo de TDAH leve. Pontuação Alta (33+ pontos): Dificuldades significativas em manter e ajustar estratégias cognitivas, impulsividade e falhas no controle atencional, compatível com diagnóstico de TDAH.\n\n**Conclusão:** O Wisconsin Card Sorting Test (WCST) é uma ferramenta poderosa para avaliar funções executivas e pode ser especialmente útil na avaliação do TDAH.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Wisconsin Card Sorting Test (WCST)",
          "autores": "Berg, E. A.",
          "ano": 1948
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Identificação de Mudança de Estratégia",
          "descricao": "(Flexibilidade Cognitiva)",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Durante o teste, o indivíduo tem dificuldade em perceber que a regra de classificação foi alterada?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Após uma mudança na regra, o indivíduo continua classificando os cartões de acordo com a regra anterior, mesmo após feedback negativo?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "A pessoa demora mais do que o esperado para alterar sua estratégia de classificação após receber feedback?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Mostra frustração ou impaciência ao perceber que sua estratégia anterior está errada?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O indivíduo falha em perceber rapidamente que deve mudar a estratégia de classificação quando confrontado com uma nova regra?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            }
          ]
        },
        {
          "titulo": "2. Impulsividade e Controle Cognitivo",
          "descricao": None,
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Durante o teste, o indivíduo toma decisões rápidas sem considerar o feedback dado?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante classifica os cartões de maneira inconsistente, mudando frequentemente de critério sem refletir sobre a estratégia?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O indivíduo se corrige após erros, mas ainda não consegue manter uma classificação consistente durante o teste?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Mostra dificuldades em fazer ajustes baseados em falhas anteriores ou feedback negativo?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante persiste em estratégias inadequadas mesmo quando o número de erros aumenta?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            }
          ]
        },
        {
          "titulo": "3. Tomada de Decisão e Monitoramento de Erros",
          "descricao": None,
          "ordem": 3,
          "perguntas": [
            {
              "texto": "O indivíduo comete erros de forma consistente durante o teste e parece incapaz de monitorar ou corrigir esses erros?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Quando informado de um erro, o indivíduo tenta adaptar a estratégia imediatamente ou continua repetindo o mesmo erro?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante toma mais tempo do que o esperado para tomar uma decisão sobre onde classificar os cartões, demonstrando indecisão?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O indivíduo consegue revisar e corrigir suas respostas de maneira autônoma, sem assistência externa?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Quando o feedback é dado, o indivíduo altera seu comportamento de forma eficiente para melhorar o desempenho?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            }
          ]
        },
        {
          "titulo": "4. Eficiência e Conclusão do Teste",
          "descricao": None,
          "ordem": 4,
          "perguntas": [
            {
              "texto": "O indivíduo demonstra dificuldades em completar a tarefa dentro do tempo estipulado, mesmo após ter entendido o conceito?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O participante se distrai facilmente e não consegue manter a concentração até o final do teste?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 2,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "A pessoa consegue classificar os cartões corretamente sem precisar de várias tentativas?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 3,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Durante o teste, o indivíduo pode perder rapidamente o foco devido a estímulos externos ou outras distrações?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 4,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "O indivíduo demonstra perseverança ao completar o teste, mesmo quando enfrenta dificuldades, sem desistir?",
              "tipo_resposta": "escala_likert_3",
              "metodo_pontuacao": "soma_item",
              "ordem": 5,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "Comportamento nunca ou raramente observado.",
                  "valor": 0,
                  "ordem": 1
                },
                {
                  "texto": "Comportamento ocasionalmente observado.",
                  "valor": 1,
                  "ordem": 2
                },
                {
                  "texto": "Comportamento frequentemente observado.",
                  "valor": 2,
                  "ordem": 3
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Escala de Avaliação de Seletividade Alimentar em Crianças com Autismo",
      "descricao": "A seletividade alimentar é um comportamento comum em crianças com Transtorno do Espectro Autista (TEA), caracterizado pela preferência ou aversão a certos tipos de alimentos. Para avaliar a seletividade alimentar em crianças com autismo, é importante considerar diversos fatores, como as preferências alimentares, a variedade da dieta, a textura e a cor dos alimentos, bem como os comportamentos que envolvem a recusa alimentar.\n\n**Instruções:** Para cada alimento apresentado à criança, observe os seguintes critérios e marque a resposta mais apropriada. A escala pode ser adaptada conforme o tipo de alimentos (sólidos ou líquidos), a idade da criança e as características específicas de cada caso.\n\n**Totalização da Escala:** Some os pontos obtidos em cada categoria. Total possível: 30 pontos.\n- 0-9 pontos: Seletividade alimentar grave.\n- 10-19 pontos: Seletividade alimentar moderada.\n- 20-30 pontos: Seletividade alimentar leve ou ausência significativa de seletividade.\n\n**Considerações Finais:** A avaliação deve ser feita de forma contínua, pois as preferências alimentares podem mudar com o tempo. É fundamental que os pais e cuidadores estejam envolvidos no processo, fornecendo informações detalhadas sobre os comportamentos alimentares da criança. Caso a seletividade alimentar seja identificada, um plano de intervenção pode ser desenvolvido em conjunto com profissionais como nutricionistas, terapeutas ocupacionais e psicólogos. Essa escala pode ser adaptada conforme o contexto e as necessidades específicas da criança, ajudando a monitorar e planejar estratégias para melhorar a alimentação.",
      "versao": "1.0",
      "fontes_literatura": [
        {
          "titulo": "Escala Autoral",
          "autores": "Não especificado",
          "ano": "Não especificado"
        }
      ],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Preferência Alimentar",
          "descricao": "Avalia a aceitação ou rejeição de certos alimentos.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Avalie o nível de preferência alimentar da criança:",
              "tipo_resposta": "escala_likert_5",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1: A criança recusa todos os alimentos apresentados.",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2: A criança recusa a maioria dos alimentos apresentados, com exceção de alguns poucos específicos.",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3: A criança aceita alguns alimentos, mas possui forte preferência por uma variedade restrita.",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4: A criança apresenta uma variedade razoável de alimentos preferidos, mas ainda tem alimentos evitados.",
                  "valor": 4.0,
                  "ordem": 4
                },
                {
                  "texto": "5: A criança aceita uma variedade ampla de alimentos e tem poucas preferências restritas.",
                  "valor": 5.0,
                  "ordem": 5
                }
              ]
            }
          ]
        },
        {
          "titulo": "2. Variedade Alimentar",
          "descricao": "Avalia a diversidade de alimentos consumidos pela criança.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Avalie o nível de variedade alimentar da criança:",
              "tipo_resposta": "escala_likert_5",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1: A criança consome apenas 1-2 alimentos específicos e rejeita todos os outros.",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2: A criança consome entre 3-5 alimentos, mas recusa a maioria das outras opções.",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3: A criança consome uma variedade moderada de alimentos (6-10), mas com preferências marcadas.",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4: A criança aceita uma boa variedade de alimentos, mas com algumas restrições em tipos de alimentos.",
                  "valor": 4.0,
                  "ordem": 4
                },
                {
                  "texto": "5: A criança consome uma ampla variedade de alimentos (mais de 10 diferentes) e experimenta novos.",
                  "valor": 5.0,
                  "ordem": 5
                }
              ]
            }
          ]
        },
        {
          "titulo": "3. Textura e Consistência dos Alimentos",
          "descricao": "Avalia a aceitação de diferentes texturas e consistências de alimentos.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "Avalie o nível de aceitação da criança em relação à textura e consistência dos alimentos:",
              "tipo_resposta": "escala_likert_5",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1: A criança recusa todas as texturas de alimentos, aceitando apenas alimentos de uma única textura (ex.: líquidos).",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2: A criança aceita apenas uma ou duas texturas, com aversão clara a outras (ex.: só aceita alimentos sólidos de textura macia).",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3: A criança é seletiva com texturas, mas aceita uma variedade de texturas limitadas (ex.: só alimentos crocantes ou moles).",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4: A criança aceita diferentes texturas de alimentos, mas com preferência por algumas (ex.: aceita alimentos crocantes, mas recusa alimentos pegajosos).",
                  "valor": 4.0,
                  "ordem": 4
                },
                {
                  "texto": "5: A criança aceita facilmente diversas texturas e consistências, mostrando interesse em explorar diferentes formas de alimentos.",
                  "valor": 5.0,
                  "ordem": 5
                }
              ]
            }
          ]
        },
        {
          "titulo": "4. Cor dos Alimentos",
          "descricao": "Avalia a preferência ou aversão a diferentes cores de alimentos.",
          "ordem": 4,
          "perguntas": [
            {
              "texto": "Avalie o nível de preferência/aversão da criança em relação à cor dos alimentos:",
              "tipo_resposta": "escala_likert_5",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1: A criança recusa alimentos de cores diferentes das que ela já aceita.",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2: A criança tem aversão a alimentos de cores específicas (ex.: recusa alimentos de cor verde).",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3: A criança aceita alimentos de diferentes cores, mas com preferência por cores específicas (ex.: prefere alimentos amarelos ou vermelhos).",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4: A criança não tem aversão à cor, mas apresenta algumas preferências mais marcadas.",
                  "valor": 4.0,
                  "ordem": 4
                },
                {
                  "texto": "5: A criança aceita alimentos de todas as cores, sem restrições.",
                  "valor": 5.0,
                  "ordem": 5
                }
              ]
            }
          ]
        },
        {
          "titulo": "5. Comportamento Durante a Alimentação",
          "descricao": "Avalia os comportamentos observados enquanto a criança está comendo.",
          "ordem": 5,
          "perguntas": [
            {
              "texto": "Avalie o comportamento da criança durante a alimentação:",
              "tipo_resposta": "escala_likert_5",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1: A criança apresenta forte resistência ou crises de comportamento (ex.: birras, agressividade) quando é apresentada uma nova comida.",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2: A criança apresenta resistência moderada a novos alimentos ou alimentos diferentes.",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3: A criança tenta experimentar novos alimentos com alguma relutância, mas sem grandes crises.",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4: A criança aceita experimentar novos alimentos com pouca resistência, sem grandes problemas comportamentais.",
                  "valor": 4.0,
                  "ordem": 4
                },
                {
                  "texto": "5: A criança demonstra curiosidade e disposição para experimentar novos alimentos sem mostrar resistência.",
                  "valor": 5.0,
                  "ordem": 5
                }
              ]
            }
          ]
        },
        {
          "titulo": "6. Tempo de Alimentação",
          "descricao": "Avalia a duração do tempo que a criança passa em uma refeição.",
          "ordem": 6,
          "perguntas": [
            {
              "texto": "Avalie o tempo de duração da refeição da criança:",
              "tipo_resposta": "escala_likert_5",
              "metodo_pontuacao": "soma_item",
              "ordem": 1,
              "is_obrigatoria": True,
              "alternativas": [
                {
                  "texto": "1: A refeição é extremamente difícil, com longos períodos de recusa e resistência.",
                  "valor": 1.0,
                  "ordem": 1
                },
                {
                  "texto": "2: A refeição pode ser muito longa devido à recusa ou ao comportamento de rejeição contínuo.",
                  "valor": 2.0,
                  "ordem": 2
                },
                {
                  "texto": "3: A refeição tem duração razoável, com a criança comendo lentamente ou com intervalos de recusa.",
                  "valor": 3.0,
                  "ordem": 3
                },
                {
                  "texto": "4: A refeição é moderadamente eficiente, com a criança comendo em um tempo mais adequado, mas com pausas.",
                  "valor": 4.0,
                  "ordem": 4
                },
                {
                  "texto": "5: A refeição é realizada de forma tranquila e dentro de um tempo normal, com a criança comendo de forma contínua.",
                  "valor": 5.0,
                  "ordem": 5
                }
              ]
            }
          ]
        }
      ]
    },
    {
      "titulo": "Questionário Detalhado de Perfil Básico de Saúde",
      "descricao": "Este questionário tem como objetivo coletar informações detalhadas sobre o perfil de saúde.",
      "versao": "2.1",
      "fontes_literatura": [],
      "is_active": True,
      "sessoes": [
        {
          "titulo": "1. Dados Pessoais",
          "descricao": "Informações básicas de identificação.",
          "ordem": 1,
          "perguntas": [
            {
              "texto": "Nome Completo:",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 1,
              "alternativas": []
            },
            {
              "texto": "Data de Nascimento (DD/MM/AAAA):",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 2,
              "alternativas": []
            },
            {
              "texto": "Sexo:",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 3,
              "alternativas": [
                {
                  "texto": "Masculino",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Feminino",
                  "valor": 0.0,
                  "ordem": 2
                },
                {
                  "texto": "Outro",
                  "valor": 0.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Nome da Mãe:",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 4,
              "alternativas": []
            },
            {
              "texto": "Nome do Pai:",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 5,
              "alternativas": []
            },
            {
              "texto": "Endereço Completo:",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 6,
              "alternativas": []
            },
            {
              "texto": "Telefone para Contato (com DDD):",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 7,
              "alternativas": []
            },
            {
              "texto": "Profissão:",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 8,
              "alternativas": []
            },
            {
              "texto": "Escolaridade:",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 9,
              "alternativas": [
                {
                  "texto": "Ensino Fundamental Incompleto",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Ensino Fundamental Completo",
                  "valor": 0.0,
                  "ordem": 2
                },
                {
                  "texto": "Ensino Médio Incompleto",
                  "valor": 0.0,
                  "ordem": 3
                },
                {
                  "texto": "Ensino Médio Completo",
                  "valor": 0.0,
                  "ordem": 4
                },
                {
                  "texto": "Ensino Superior Incompleto",
                  "valor": 0.0,
                  "ordem": 5
                },
                {
                  "texto": "Ensino Superior Completo",
                  "valor": 0.0,
                  "ordem": 6
                },
                {
                  "texto": "Pós-graduação",
                  "valor": 0.0,
                  "ordem": 7
                }
              ]
            }
          ]
        },
        {
          "titulo": "2. Informações Físicas",
          "descricao": "Medidas e características físicas.",
          "ordem": 2,
          "perguntas": [
            {
              "texto": "Peso (kg):",
              "tipo_resposta": "numerica",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 1,
              "alternativas": []
            },
            {
              "texto": "Altura (cm):",
              "tipo_resposta": "numerica",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 2,
              "alternativas": []
            },
            {
              "texto": "Tipo Sanguíneo:",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 3,
              "alternativas": [
                {
                  "texto": "A+",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "A-",
                  "valor": 0.0,
                  "ordem": 2
                },
                {
                  "texto": "B+",
                  "valor": 0.0,
                  "ordem": 3
                },
                {
                  "texto": "B-",
                  "valor": 0.0,
                  "ordem": 4
                },
                {
                  "texto": "AB+",
                  "valor": 0.0,
                  "ordem": 5
                },
                {
                  "texto": "AB-",
                  "valor": 0.0,
                  "ordem": 6
                },
                {
                  "texto": "O+",
                  "valor": 0.0,
                  "ordem": 7
                },
                {
                  "texto": "O-",
                  "valor": 0.0,
                  "ordem": 8
                },
                {
                  "texto": "Não sei",
                  "valor": 0.0,
                  "ordem": 9
                }
              ]
            }
          ]
        },
        {
          "titulo": "3. Hábitos e Estilo de Vida",
          "descricao": "Informações sobre hábitos diários.",
          "ordem": 3,
          "perguntas": [
            {
              "texto": "Você fuma?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 1,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Quantos cigarros por dia (aproximadamente)? (Se sim)",
              "tipo_resposta": "numerica",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 2,
              "alternativas": []
            },
            {
              "texto": "Você consome bebidas alcoólicas?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 3,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Com que frequência você consome bebidas alcoólicas?",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 4,
              "alternativas": []
            },
            {
              "texto": "Pratica alguma atividade física regularmente?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 5,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Qual atividade física? (Se sim)",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 6,
              "alternativas": []
            },
            {
              "texto": "Quantas vezes por semana? (Se sim)",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 7,
              "alternativas": []
            },
            {
              "texto": "Você tem um sono regular?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 8,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Quantas horas você dorme por noite, em média?",
              "tipo_resposta": "numerica",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 9,
              "alternativas": []
            }
          ]
        },
        {
          "titulo": "4. Histórico de Saúde",
          "descricao": "Informações sobre condições médicas e histórico familiar.",
          "ordem": 4,
          "perguntas": [
            {
              "texto": "Quais comorbidades você possui? (Selecione todas que se aplicam)",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 1,
              "alternativas": [
                {
                  "texto": "Hipertensão",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Diabetes",
                  "valor": 0.0,
                  "ordem": 2
                },
                {
                  "texto": "Doenças Cardíacas",
                  "valor": 0.0,
                  "ordem": 3
                },
                {
                  "texto": "Asma",
                  "valor": 0.0,
                  "ordem": 4
                },
                {
                  "texto": "Alergias",
                  "valor": 0.0,
                  "ordem": 5
                },
                {
                  "texto": "Outras",
                  "valor": 0.0,
                  "ordem": 6
                }
              ]
            },
            {
              "texto": "Detalhe outras comorbidades:",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 2,
              "alternativas": []
            },
            {
              "texto": "Você faz uso de alguma medicação contínua?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 3,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Quais medicações? (Caso sim)",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 4,
              "alternativas": []
            },
            {
              "texto": "Possui alguma alergia a medicamentos?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 5,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                }
              ]
            },
            {
              "texto": "Quais medicamentos? (Caso sim)",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 6,
              "alternativas": []
            },
            {
              "texto": "Histórico familiar de doenças cardíacas?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 7,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                },
                {
                  "texto": "Não sei",
                  "valor": 0.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Histórico familiar de diabetes?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 8,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                },
                {
                  "texto": "Não sei",
                  "valor": 0.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Histórico familiar de câncer?",
              "tipo_resposta": "escolha_personalizada",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 9,
              "alternativas": [
                {
                  "texto": "Sim",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "Não",
                  "valor": 0.0,
                  "ordem": 2
                },
                {
                  "texto": "Não sei",
                  "valor": 0.0,
                  "ordem": 3
                }
              ]
            },
            {
              "texto": "Qual tipo de câncer? (Caso sim)",
              "tipo_resposta": "texto_puro",
              "is_obrigatoria": False,
              "metodo_pontuacao": "N/D",
              "ordem": 10,
              "alternativas": []

            }
          ]
        },
        {
          "titulo": "5. Avaliação da Dor (Escala Visual Analógica - EVA)",
          "descricao": "Use a escala de 0 a 10 para indicar sua dor.",
          "ordem": 5,
          "perguntas": [
            {
              "texto": "Nível de dor atual (0 = Sem dor, 10 = Dor máxima):",
              "tipo_resposta": "escala_likert_10",
              "is_obrigatoria": True,
              "metodo_pontuacao": "N/D",
              "ordem": 1,
              "alternativas": [
                {
                  "texto": "0",
                  "valor": 0.0,
                  "ordem": 1
                },
                {
                  "texto": "1",
                  "valor": 0.0,
                  "ordem": 2
                },
                {
                  "texto": "2",
                  "valor": 0.0,
                  "ordem": 3
                },
                {
                  "texto": "3",
                  "valor": 0.0,
                  "ordem": 4
                },
                {
                  "texto": "4",
                  "valor": 0.0,
                  "ordem": 5
                },
                {
                  "texto": "5",
                  "valor": 0.0,
                  "ordem": 6
                },
                {
                  "texto": "6",
                  "valor": 0.0,
                  "ordem": 7
                },
                {
                  "texto": "7",
                  "valor": 0.0,
                  "ordem": 8
                },
                {
                  "texto": "8",
                  "valor": 0.0,
                  "ordem": 9
                },
                {
                  "texto": "9",
                  "valor": 0.0,
                  "ordem": 10
                },
                {
                  "texto": "10",
                  "valor": 0.0,
                  "ordem": 11
                }
              ]
            }
          ]
        }
      ]
    }
  ]

def popular_banco():
    """
    Rota para popular o banco de dados com os questionários do arquivo JSON.
    """
    logging.info("Iniciando a população do banco de dados...")
    try:
 
        questionarios_criados = 0
        sessoes_criadas = 0
        perguntas_criadas = 0
        alternativas_criadas = 0
        logging.log
        # Itera sobre os questionários no JSON
        logging.info("iterando sobre questionarios")
        for questionario_data in questionarios:
            logging.info("criando questionario: %s", questionario_data['titulo'])
            # Verifica se o questionário já existe
            questionario_existente = db.session.query(Questionario).filter_by(
                titulo=questionario_data['titulo'],
                versao=questionario_data['versao']
            ).first()

            if questionario_existente:
                continue  # Pula se já existir

            # Cria um novo questionário
            novo_questionario = Questionario(
                titulo=questionario_data['titulo'],
                descricao=questionario_data['descricao'],
                versao=questionario_data['versao'],
                fontes_literatura=questionario_data.get('fontes_literatura', []),
                is_active=questionario_data['is_active']
            )
            db.session.add(novo_questionario)
            db.session.commit()
            questionarios_criados += 1

            # Itera sobre as sessões do questionário
            for sessao_data in questionario_data['sessoes']:
                logging.info("criando sessao: %s", sessao_data['titulo'])
                nova_sessao = Sessao(
                    questionario_id=novo_questionario.id,
                    titulo=sessao_data['titulo'],
                    descricao=sessao_data['descricao'],
                    ordem=sessao_data['ordem']
                )
                db.session.add(nova_sessao)
                db.session.commit()
                sessoes_criadas += 1

                # Itera sobre as perguntas da sessão
                for pergunta_data in sessao_data['perguntas']:
                    nova_pergunta = Pergunta(
                        sessao_id=nova_sessao.id,
                        texto=pergunta_data['texto'],
                        tipo_resposta=pergunta_data['tipo_resposta'],
                        metodo_pontuacao=pergunta_data['metodo_pontuacao'],
                        ordem=pergunta_data['ordem'],
                        is_obrigatoria=pergunta_data['is_obrigatoria']
                    )
                    db.session.add(nova_pergunta)
                    db.session.commit()
                    perguntas_criadas += 1

                    # Itera sobre as alternativas da pergunta
                    for alternativa_data in pergunta_data['alternativas']:
                        nova_alternativa = Alternativa(
                            pergunta_id=nova_pergunta.id,
                            texto=alternativa_data['texto'],
                            valor=alternativa_data['valor'],
                            ordem=alternativa_data['ordem']
                        )
                        db.session.add(nova_alternativa)
                        db.session.commit()
                        alternativas_criadas += 1

        # Fecha a sessão
        db.session.close()
        
        
        logging.info("População concluida com sucesso!")
        logging.info("Informações sobre a população:")
        logging.info("Questionários criados: %s", questionarios_criados)
        logging.info("Sessões criadas: %s", sessoes_criadas)
        logging.info("Perguntas criadas: %s", perguntas_criadas)
        logging.info("Alternativas criadas: %s", alternativas_criadas)
        

    except Exception as e:
        # Em caso de erro, faz rollback e retorna mensagem de erro
        if 'session' in locals():
            db.session.rollback()
            db.session.close()

        print(f"Erro ao popular o banco de dados: {e}")
        print("População cancelada.")
        
        

if __name__ == "__main__":
    from app import create_app
    app = create_app()
    with app.app_context():
        popular_banco()