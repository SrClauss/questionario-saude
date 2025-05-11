let sessoes_modificadas = sessoes.map((sessao)=>{
    return sessao["perguntas"].map((pergunta)=>{
        return pergunta["tipo_resposta"] = "escala_likert_3"
    })
})