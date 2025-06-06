import React, { useState, useEffect, useCallback } from "react";
import {
  Box,
  Typography,
  TextField,
  Divider,
  Button,
  Modal,
  Switch,
  FormControlLabel,
  MenuItem,
  FormControl,
  Radio,
  RadioGroup,
  FormLabel
} from "@mui/material";
import { Pergunta } from "../../types/questionario";
import StylizedTitle from "../../components/StylizedTitle";
import { RegrasVisibilidadeType, RespostasEspecificasInterface, FaixaDePontuacaoInterface, RoleDoUsuarioInterface } from "../../types/questionario";

export interface SessaoData {
  id?: string;
  titulo: string;
  descricao?: string;
  ordem: number;
  regras_visibilidade?: RegrasVisibilidadeType[];
  logica_principal_entre_regras?: "AND" | "OR"; // Para carregar/salvar as novas regras
}

interface SessaoModalProps {
  open: boolean;
  onClose: () => void;
  onSave: (sessao: SessaoData) => void;
  initialData?: SessaoData;
  questionarioId: string;
  currentSessaoId?: string;
  ordem: number;
}

const SessaoModal: React.FC<SessaoModalProps> = ({
  open,
  onClose,
  onSave,
  initialData,
  questionarioId,
  currentSessaoId,
  ordem,
}) => {
  const [titulo, setTitulo] = useState(initialData?.titulo || "");
  const [descricao, setDescricao] = useState(initialData?.descricao || "");
  const [tiposRegraSelecionados, setTiposRegraSelecionados] = useState<string[]>([]); // Alterado para array
  const [allPerguntas, setAllPerguntas] = useState<Pergunta[]>([]);
  const [showConditional, setShowConditional] = useState(!!initialData?.regras_visibilidade === true);
  const [logicaPrincipalEntreRegras, setLogicaPrincipalEntreRegras] = useState<"AND" | "OR">("AND");
  const [regras, setRegras] = useState<RegrasVisibilidadeType[]>(initialData?.regras_visibilidade || []);

  // Busca as perguntas condicionais se o switch estiver ativo.
  useEffect(() => {
    if (!open) return;
    if (!showConditional) {
      setAllPerguntas([]); // Limpa as perguntas se a lógica condicional for desabilitada
      return;
    }
    const effectiveQId = questionarioId || (initialData && (initialData as any).questionario_id);
    if (!effectiveQId) {
      console.error("questionarioId não foi definido.");
      return;
    }
    fetch(`${import.meta.env.VITE_BACKEND_URL}/questionario/detailed/${effectiveQId}`, {
      headers: { Authorization: `Bearer ${localStorage.getItem("@App:token")}` }
    })
      .then(res => res.json())
      .then((data) => {
        if (!data.sessoes || !Array.isArray(data.sessoes)) {
          console.error("Propriedade 'sessoes' não encontrada na resposta:", data);
          return;
        }
        const perguntas: Pergunta[] = [];
        data.sessoes.forEach((sessao: any) => {
          if (sessao.id !== currentSessaoId && sessao.perguntas && Array.isArray(sessao.perguntas)) {
            perguntas.push(...sessao.perguntas);
          }
        });
        setAllPerguntas(perguntas);
      })
      .catch(console.error);
  }, [open, showConditional, questionarioId, currentSessaoId, initialData]); // initialData pode ser necessário se contiver questionario_id

  // Reseta os estados quando initialData muda
  useEffect(() => {
    setTitulo(initialData?.titulo || "");
    setDescricao(initialData?.descricao || "");
    setTiposRegraSelecionados([]);
    setShowConditional(!!initialData?.regras_visibilidade);
    const loadedRegras = (initialData as any)?.regras_visibilidade || [];
    setRegras(loadedRegras);
    if (loadedRegras.length > 0) {
      const tipos = loadedRegras
        .map((r: RegrasVisibilidadeType) => r.tipo_regra)
        .filter((value: string, index: number, self: string[]) => self.indexOf(value) === index); // Unique types
      setTiposRegraSelecionados(tipos);
      // Poderia também carregar logicaPrincipalEntreRegras se estiver no initialData
    } else {
      setTiposRegraSelecionados([]);
    }
  }, [initialData]);

  // Efeito para remover regras do estado quando o tipo de regra é desmarcado
  useEffect(() => {
    setRegras(prevRegras =>
      prevRegras.filter(regra =>
        tiposRegraSelecionados.includes(regra.tipo_regra)
      )
    );
  }, [tiposRegraSelecionados]);
  const handleSetRegra = useCallback((novaRegra: RegrasVisibilidadeType) => {
    setRegras(prevRegras => {
      if (!novaRegra.tipo_regra) {
        console.warn("Regra sem tipo_regra recebida:", novaRegra);
        return prevRegras;
      }
      const tipoDaNovaRegra = novaRegra.tipo_regra;

      const existingRuleIndex = prevRegras.findIndex(r => r.tipo_regra === tipoDaNovaRegra);

      if (existingRuleIndex > -1) {
        const updatedRegras = [...prevRegras];
        updatedRegras[existingRuleIndex] = novaRegra;
        return updatedRegras;
      } else {
        return [...prevRegras, novaRegra];
      }
    });
  }, [setRegras]); // setRegras é estável

  const handleSave = () => {
    const sessaoPayload: SessaoData = {
      titulo,
      descricao: descricao || undefined, // Envia undefined se vazio para não salvar string vazia
      ordem: initialData?.ordem ?? ordem, // Usa a ordem inicial se editando, ou a nova ordem se criando
    };

    if (showConditional) {
      sessaoPayload.regras_visibilidade = regras;
      sessaoPayload.logica_principal_entre_regras = logicaPrincipalEntreRegras;
      // Adicionar logicaPrincipalEntreRegras ao payload se necessário pela API
      // sessaoPayload.logica_principal_entre_regras = logicaPrincipalEntreRegras;
    } else {
      sessaoPayload.regras_visibilidade = []; // Ou undefined, dependendo da API
    }

    onSave(sessaoPayload);
    onClose();
  };


  return (
    <Modal open={open} onClose={onClose}>
      <Box sx={{
        backgroundColor: "white",
        width: { xs: "90%", sm: "60%", md: "40%" },
        margin: "auto",
        padding: 3,
        borderRadius: 2,
        maxHeight: "90vh",
        overflowY: "auto",
      }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          {initialData ? "Editar Sessão" : "Nova Sessão"}
        </Typography>
        <TextField
          label="Título"
          fullWidth
          value={titulo}
          onChange={e => setTitulo(e.target.value)}
          margin="normal"
        />
        <TextField
          label="Descrição"
          fullWidth
          multiline
          rows={3}
          value={descricao}
          onChange={e => setDescricao(e.target.value)}
          margin="normal"
        />
        <Divider sx={{ my: 2 }} />
        <FormControlLabel
          control={
            <Switch
              checked={showConditional}
              onChange={(e) => {
                setShowConditional(e.target.checked);
                if (!e.target.checked) {
                  // Limpa os valores caso desabilite
                  setTiposRegraSelecionados([]);
                  setRegras([]);
                }
              }}
              color="primary"
            />
          }

          label="Habilitar condições (Pergunta e Respostas Condicionais)"
        />
        {showConditional && (
          <>
          <Box sx={{ alignItems: "center", gap: 1, mb: 1 }}>
            <TextField
              select
              label="Tipo de regra"
              fullWidth
              value={tiposRegraSelecionados} // Usar o estado do array
              onChange={(e) => {
                const value = e.target.value;
                // O valor será um array de strings quando multiple=true
                setTiposRegraSelecionados(typeof value === 'string' ? value.split(',') : value);
              }}
              margin="normal"
              slotProps={{
                select: {
                  multiple: true


                }
              }}


            >
              <MenuItem value="RESPOSTA_ESPECIFICA">Resposta Específica</MenuItem>
              <MenuItem value="FAIXA_DE_PONTUACAO">Faixa de Pontuação</MenuItem>
              <MenuItem value="ROLE_USUARIO">Role do Usuário</MenuItem>



            </TextField>



            
            <FormLabel component="legend">Lógica principal entre regras</FormLabel>
            <RadioGroup
              row
              value={logicaPrincipalEntreRegras}
              onChange={(e) => {
                const value = e.target.value;
                if (value === "AND" || value === "OR") {
                  setLogicaPrincipalEntreRegras(value);
                }
              }}
            >
              <FormControlLabel value="AND" control={<Radio />} label="AND" />
              <FormControlLabel value="OR" control={<Radio />} label="OR" />
            </RadioGroup>
          </Box>  
          {
            tiposRegraSelecionados.includes("RESPOSTA_ESPECIFICA") &&
            (
              <RespostasEspecificas
                onSetData={handleSetRegra}
                allPerguntas={allPerguntas}
                initialRuleData={regras.find(r => r.tipo_regra === "RESPOSTA_ESPECIFICA") as RespostasEspecificasInterface | undefined}
              />
            )
          }

          {
            tiposRegraSelecionados.includes("FAIXA_DE_PONTUACAO") &&
            (
              <FaixaDePontuacao
                onSetData={handleSetRegra}
                allPerguntas={allPerguntas}
                initialRuleData={regras.find(r => r.tipo_regra === "FAIXA_DE_PONTUACAO") as FaixaDePontuacaoInterface | undefined}
              />
            )
          }

          {
            tiposRegraSelecionados.includes("ROLE_USUARIO") &&
            (
              <RoleDoUsuario
                onSetData={handleSetRegra}
                allPerguntas={[]} // RoleDoUsuario não usa allPerguntas
                initialRuleData={regras.find(r => r.tipo_regra === "ROLE_USUARIO") as RoleDoUsuarioInterface | undefined}
              />
            )
          }
        
          </>
        )}


        <Divider sx={{ my: 2 }} />
        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 1, mt: 2 }}>
          <Button variant="outlined" onClick={onClose}>Cancelar</Button>
          <Button variant="contained" onClick={handleSave}>Salvar</Button>
        </Box>
      </Box>
    </Modal>
  );
};


export interface RuleComponentProps {
  onSetData: (data: any) => void;
  allPerguntas: Pergunta[];
  initialRuleData?: RegrasVisibilidadeType; // Prop genérica para dados iniciais
}



function RespostasEspecificas({ onSetData, allPerguntas, initialRuleData }: RuleComponentProps) {

  const [perguntaAlvoId, setPerguntaAlvoId] = useState<string>("");
  const [respostasNecessariasIds, setRespostasNecessariasIds] = useState<string[]>([]);
  const [logicaRespostas, setLogicaRespostas] = useState<"AND" | "OR">("OR");
  const typedInitialData = initialRuleData as RespostasEspecificasInterface | undefined;

  useEffect(() => {
    if (perguntaAlvoId) { // Só envia se uma pergunta alvo estiver selecionada
      const dataPayload: RespostasEspecificasInterface = {
        tipo_regra: "RESPOSTA_ESPECIFICA",
        pergunta_alvo_id: perguntaAlvoId,
        respostas_necessarias_ids: respostasNecessariasIds,
        logica_respostas: logicaRespostas,
      };
      onSetData(dataPayload);
    }
    // Considerar limpar a regra no pai se perguntaAlvoId for desmarcado
  }, [perguntaAlvoId, respostasNecessariasIds, logicaRespostas, onSetData]);

  useEffect(() => {
    if (typedInitialData) {
      setPerguntaAlvoId(typedInitialData.pergunta_alvo_id || "");
      setRespostasNecessariasIds(typedInitialData.respostas_necessarias_ids || []);
      setLogicaRespostas(typedInitialData.logica_respostas || "OR");
    } else {
      // Resetar se não houver dados iniciais (ex: regra desmarcada e remarcada)
      // setPerguntaAlvoId(""); setRespostasNecessariasIds([]); setLogicaRespostas("OR"); // Opcional, depende do comportamento desejado
    }
  }, [typedInitialData]);

  return (
    <Box sx={{ mt: 2 }}>

    <StylizedTitle title={"Respostas Específicas"} size="h6"/>
    <FormControl component="fieldset" margin="normal" fullWidth>
        <FormLabel component="legend">Lógica entre Respostas Necessárias</FormLabel>
        <RadioGroup row value={logicaRespostas} onChange={(e) => setLogicaRespostas(e.target.value as "AND" | "OR")}>
          <FormControlLabel value="AND" control={<Radio />} label="E (todas selecionadas)" />
          <FormControlLabel value="OR" control={<Radio />} label="OU (qualquer uma selecionada)" />
        </RadioGroup>
      </FormControl>
    <TextField
      select
      label="Pergunta alvo"
      fullWidth
      value={perguntaAlvoId}
      onChange={(e) => {
        setPerguntaAlvoId(e.target.value);
      }}
      margin="normal"
      slotProps={{
        select: {
          multiple: false
        }
        }}
    >
      {allPerguntas.map((pergunta) => (
        <MenuItem key={pergunta.id} value={pergunta.id}>
          {pergunta.texto}
        </MenuItem>
      ))}


    </TextField>
      {perguntaAlvoId && (
        <TextField
          select
          label="Respostas necessárias"
          fullWidth
          value={respostasNecessariasIds}
          onChange={(event) => {
            const {
              target: { value },
            } = event;
            setRespostasNecessariasIds(
              // On autofill we get a stringified value.
              typeof value === 'string' ? value.split(',') : value,
            );
          }}
          margin="normal"

          slotProps={{
            select: {
              multiple: true
            }
          }}
      
        >
          {(allPerguntas.find(p => p.id === perguntaAlvoId)?.alternativas || []).map((alternativa) => (
            <MenuItem key={alternativa.id} value={alternativa.id}>
              {alternativa.texto}
            </MenuItem>
          ))}
        </TextField>
      )}
    </Box>
   
  )

}


function FaixaDePontuacao({ onSetData, allPerguntas, initialRuleData }: RuleComponentProps) {
  const [perguntasParaCalculoIds, setPerguntasParaCalculoIds] = useState<string[]>([]);
  const [pontuacaoMinima, setPontuacaoMinima] = useState<number>(0); 
  const [pontuacaoMaxima, setPontuacaoMaxima] = useState<number>(10); 
  const typedInitialData = initialRuleData as FaixaDePontuacaoInterface | undefined;

  // Efeito para comunicar as mudanças ao componente pai
  useEffect(() => {
    const dataPayload: FaixaDePontuacaoInterface = {
      tipo_regra: "FAIXA_DE_PONTUACAO",
      perguntas_para_calculo_ids: perguntasParaCalculoIds,
      pontuacao_minima_exigida: Number(pontuacaoMinima),
      pontuacao_maxima_exigida: Number(pontuacaoMaxima),
    };
    onSetData(dataPayload);
  }, [perguntasParaCalculoIds, pontuacaoMinima, pontuacaoMaxima, onSetData]);

  useEffect(() => {
    if (typedInitialData) {
      setPerguntasParaCalculoIds(typedInitialData.perguntas_para_calculo_ids || []);
      setPontuacaoMinima(typedInitialData.pontuacao_minima_exigida ?? 0);
      setPontuacaoMaxima(typedInitialData.pontuacao_maxima_exigida ?? 10);
    } else {
      // Resetar se não houver dados iniciais
      // setPerguntasParaCalculoIds([]); setPontuacaoMinima(0); setPontuacaoMaxima(10); // Opcional
    }
  }, [typedInitialData]);

  return (
    <Box sx={{ mt: 2 }}>
      <StylizedTitle title={"Faixa de Pontuação"} size="h6" />
      <TextField
        select
        label="Perguntas para cálculo da pontuação"
        fullWidth
        value={perguntasParaCalculoIds}
        onChange={(event) => {
          const {
            target: { value },
          } = event;
          setPerguntasParaCalculoIds(
            typeof value === 'string' ? value.split(',') : value,
          );
        }}
        margin="normal"
        slotProps={
          {
            select: {
              multiple: true
            }
          }
        }
       
      >
        {allPerguntas.map((pergunta) => (
          <MenuItem key={pergunta.id} value={pergunta.id}>
            {pergunta.texto}
          </MenuItem>
        ))}
      </TextField>
      <Box sx={{ display: 'flex', gap: 2, mt: 1 }}>
        <TextField 
          label="Pontuação mínima" 
          type="number" 
          fullWidth 
          value={pontuacaoMinima} 
          onChange={(e) => setPontuacaoMinima(Number(e.target.value))} 
          margin="normal" 
        />
        <TextField 
          label="Pontuação máxima" 
          type="number" 
          fullWidth 
          value={pontuacaoMaxima} 
          onChange={(e) => setPontuacaoMaxima(Number(e.target.value))} 
          margin="normal" 

        />
      </Box>
    </Box>
  );
}

function RoleDoUsuario({ onSetData, initialRuleData }: RuleComponentProps) { // allPerguntas removido pois não é usado
  const [rolesPermitidos, setRolesPermitidos] = useState<string[]>([]);
  const typedInitialData = initialRuleData as RoleDoUsuarioInterface | undefined;

  // Efeito para comunicar as mudanças ao componente pai
  useEffect(() => {
    const dataPayload: RoleDoUsuarioInterface = {
      tipo_regra: "ROLE_USUARIO",
      roles_permitidos: rolesPermitidos,
    };
    onSetData(dataPayload);
  }, [rolesPermitidos, onSetData]);

  useEffect(() => {
    if (typedInitialData) {
      setRolesPermitidos(typedInitialData.roles_permitidos || []);
    } else {
      // Resetar se não houver dados iniciais
      // setRolesPermitidos([]); // Opcional
    }
  }, [typedInitialData]);

  return (
    <Box sx={{ mt: 2 }}>
      <StylizedTitle title={"Role do Usuário"} size="h6" />
      <TextField
        select
        label="Roles permitidas"
        fullWidth
        value={rolesPermitidos}
        onChange={(event) => {
          const {
            target: { value },
          } = event;
          setRolesPermitidos(
            typeof value === 'string' ? value.split(',') : value,
          );
        }}
        margin="normal"
        slotProps={
          {
            select: {
              multiple: true
            }
          }
        }
        
        >
          <MenuItem value={"paciente"}>Paciente</MenuItem>
          <MenuItem value={"profissional_saude"}>Terapeuta</MenuItem>

        </TextField>
    </Box>
  );

}


export default SessaoModal;
