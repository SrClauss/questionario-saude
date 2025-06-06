import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { Avaliacao } from "../types/avaliacao";
import { BateriaTestes } from "../types/baterias";
import { Medico, Paciente } from "../types/user";
import VariableLayout from "../layouts/VariableLayout";
import { Questionario } from "../types/questionario";
import { UnidadeSaude } from "../types/unidade_saude";
import CardAvaliacao from "../components/CardAvaliacao";
import BateriasCadastroModal from "../modals/BateriasCadastroModal";
import { Box, Fab, Tooltip } from "@mui/material";
import { auth } from "../utils/auth";
import ConfirmActionModal from "../modals/ConfirmActionModal";
import ProntuarioIconComponent from "../components/ProntuarioIconComponent";
import AvaliacaoModal from "../modals/AvaliacaoModal";
import AtribuirMedicoModal from "../modals/AtribuirMedicoModal";
//crie um tipo que represente uma avaliação joinada com as baterias testes, paciente e unidade saude
interface AvaliacaoJoin extends Avaliacao {
  avaliacao: Avaliacao;
  baterias_testes: BateriasTestesJoin[];
  paciente: Paciente;
  unidade_saude: UnidadeSaude;
  medico: Medico;
}
/*
complete_obj = {
                "avaliacao": avaliacao.to_json(),
                "baterias_testes": lista_baterias_json,
                "medico": avaliacao.medico.to_json() if avaliacao.medico else None,
                "unidade_saude": avaliacao.unidade_saude.to_json() if avaliacao.unidade_saude else None,
                "paciente": avaliacao.paciente.to_json() if avaliacao.paciente else None
            }


*/
interface BateriasTestesJoin extends BateriaTestes {
  questionario: Questionario;
}
export default function AvaliacaoScreen() {
  const { paciente_id } = useParams();
  const [avaliacoesJoin, setAvaliaoesJoin] = useState<AvaliacaoJoin[]>([]);
  const [bateriaModalOpen, setBateriaModalOpen] = useState(false);

  const [medicoModalOpen, setMedicoModalOpen] = useState(false);
  const [avaliacaoModalOpen, setAvaliacaoModalOpen] = useState(false);
  const [avaliacaoSelecionada, setAvaliacaoSelecionada] = useState<
    string | null
  >(null);

  const [confirmDeleteModalOpen, setConfirmDeleteModalOpen] = useState(false);
  const [emptyPaciente, setEmptyPaciente] = useState<Paciente | null>(null);

  const handleAddBateria = async (
    questionario: string,
    data_aplicacao: string
  ) => {
    let profissionalSaudeId = null;
    const user = auth.getUserData();
    if (user && user.role === "profissional_saude") {
    
      profissionalSaudeId = auth.getProfile()?.id;
    }

    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");

    try {
      const response = await fetch(`${baseUrl}/baterias_testes`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          profissional_saude_id: profissionalSaudeId,
          paciente_id: paciente_id,
          questionario_id: questionario,
          data_aplicacao: data_aplicacao,
          avaliacao_id: avaliacaoSelecionada,
        }),
      });
      const data = await response.json();
      if (response.ok) {
        setBateriaModalOpen(false);
        fetchAvaliacaoJoin();
      } else {
        console.error("Error adding bateria:", data);
      }
    } catch (error) {
      console.error("Error adding bateria:", error);
    }

  };
  const fetchAvaliacaoJoin = async () => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    try {
      const response = await fetch(
        `${baseUrl}/avaliacoes/paciente/${paciente_id}`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = await response.json();

      if (response.ok) {
        setAvaliaoesJoin(data);
      } else {
        if (response.status === 404) {
          setAvaliaoesJoin([]);
          setEmptyPaciente(data);
        } else {
          console.error("Error fetching avaliacao join:", data);
        }
      }
    } catch (error) {
      console.error("Error fetching avaliacao join:", error);
    }
  };
  const handleDeleteAvalicao = async () => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    try {
      const response = await fetch(
        `${baseUrl}/avaliacoes/${avaliacaoSelecionada}`,
        {
          method: "DELETE",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = await response.json();

      if (response.ok) {
        setConfirmDeleteModalOpen(false);
        fetchAvaliacaoJoin();
      } else {
        console.error("Error deleting avaliacao:", data);
      }
    } catch (error) {
      console.error("Error deleting avaliacao:", error);
    } finally {
      fetchAvaliacaoJoin();
    }
  };
  const handleAtribuirMedico = async (medicoId: string, avaliacaoId: string) => {
    const baseUrl = import.meta.env.VITE_BACKEND_URL;
    const token = localStorage.getItem("@App:token");
    try {
      const response = await fetch(
        `${baseUrl}/avaliacoes/set_medico/${avaliacaoId}/${medicoId}`,
        {
          method: "PUT",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        }
      );
      const data = await response.json();

      if (response.ok) {
        setMedicoModalOpen(false);
        fetchAvaliacaoJoin();
      } else {
        console.error("Error deleting avaliacao:", data);
      }
    } catch (error) {
      console.error("Error deleting avaliacao:", error);
    }
  };
  useEffect(() => {
    fetchAvaliacaoJoin();
  }, []);

  return (
    <VariableLayout>

      <Tooltip title="Adicionar Avaliação" placement="right">
        <Fab
          color="primary"
          aria-label="add"
          sx={{
            position: "fixed",
            bottom: 64,
            right: 64,
          }}
          onClick={() => setAvaliacaoModalOpen(true)}
        >
          <ProntuarioIconComponent /> {/* Adicione um ícone ao Fab */}
        </Fab>
      </Tooltip>

      {avaliacoesJoin.length === 0 && (
        <Box
          sx={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            height: "100%",
            flexDirection: "column",
          }}
        >
          <h1>Não há avaliações cadastradas para este paciente.</h1>
        </Box>
      )}
      <Box
        sx={{
          marginTop: { xs: 6, sm: 0 },
          overflowY: "auto",
        }}
      >
        {avaliacoesJoin.map((avaliacaoJoin) => (
          <>
          
          
          <CardAvaliacao
            key={avaliacaoJoin.avaliacao.id}
            avaliacaoJoin={avaliacaoJoin}
            onOpenBateriaModal={() => {
              setAvaliacaoSelecionada(avaliacaoJoin.avaliacao.id);
              setBateriaModalOpen(true);
            }}
            onOpenLaudoModal={() => setBateriaModalOpen(true)}
            onOpenMedicoModal={() => setMedicoModalOpen(true)}
            onRefresh={fetchAvaliacaoJoin}
            onDeleteAvaliacao={() => {
              setAvaliacaoSelecionada(avaliacaoJoin.avaliacao.id);
              setConfirmDeleteModalOpen(true);
            }}
          />
          <AtribuirMedicoModal
          open={medicoModalOpen}
          avaliacaoId={avaliacaoJoin.avaliacao.id}
          onClose={() => setMedicoModalOpen(false)}
          onSubmit={handleAtribuirMedico}
        />
          </>
        ))}
        <BateriasCadastroModal
          open={bateriaModalOpen}
          onSubmit={(questionarioId, data_aplicacao) => {
            handleAddBateria(questionarioId, data_aplicacao);
            setAvaliacaoSelecionada(null);
            setBateriaModalOpen(false);
          }}
          onClose={() => {
            setBateriaModalOpen(false);
          }}
        />

        <ConfirmActionModal
          open={confirmDeleteModalOpen}
          onClose={() => setConfirmDeleteModalOpen(false)}
          onConfirm={() => {
            handleDeleteAvalicao();
            setConfirmDeleteModalOpen(false);
          }}
          confirmationText="Deletar avaliação"
          description="Tem certeza que deseja excluir essa avaliacao?, esta ação não pode ser desfeita"
          title="Excluir avaliacao"
        />
        {(emptyPaciente || avaliacoesJoin[0]?.paciente) && (
          <AvaliacaoModal
            paciente={emptyPaciente || avaliacoesJoin[0]?.paciente}
            open={avaliacaoModalOpen}
            onClose={() => {
              setAvaliacaoModalOpen(false);
              fetchAvaliacaoJoin();
            }}
            initialAvaliacao={null}
          />
        )}
  
      </Box>
    </VariableLayout>
  );
}
