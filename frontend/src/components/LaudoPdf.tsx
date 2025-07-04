// LaudoPdf.tsx
import { useEffect, useState, FC } from 'react';
import { Page, Text, View, Document, StyleSheet, PDFViewer, Image } from '@react-pdf/renderer';

// Definições de tipo
export interface MedicoLaudoInfo {
    nome: string | null;
    crm: string | null;
    especialidade: string | null;
}

export interface CidInfo {
    cid: string;
    descricao: string;
}

export interface LaudoInfo {
    id: string;
    data_emissao: string | null;
    parecer: string | null;
    abordagem_terapeutica: string | null;
    medico: MedicoLaudoInfo | null;
    cids_associados: CidInfo[];
}

export interface PacienteLaudoInfo {
    nome: string | null;
    data_nascimento: string | null;
    cpf: string | null;
    telefone?: string | null;
}

export interface UnidadeSaudeLaudoInfo {
    nome: string | null;
    cnpj?: string | null;
}

export interface AvaliacaoLaudoInfo {
    id: string;
    data_inicio: string | null;
    unidade_saude: UnidadeSaudeLaudoInfo | null;
}

export interface QuestionarioAplicadoInfo {
    questionario_id: string;
    titulo: string | null;
    data_aplicacao: string | null;
    score: number | string | null;
    fontes_literatura_formatadas: string[];
}

export interface LaudoApiData {
    laudo_info: LaudoInfo;
    paciente_info: PacienteLaudoInfo;
    avaliacao_info: AvaliacaoLaudoInfo;
    questionarios_aplicados: QuestionarioAplicadoInfo[];
    todas_referencias_bibliograficas: string[];
    qr_code_assinatura_base64?: string | null; // Adicionado como opcional
}

export interface LaudoPDFDocumentProps {
    // Modificado para receber os dados e o QR code separadamente ou dentro de um objeto específico
    laudoApiData: LaudoApiData | null;
    qrCodeBase64: string | null;
}

export interface LaudoPDFViewerProps {
    avaliacaoId: string;
}

// Estilos do documento
const styles = StyleSheet.create({
  page: { // Estilo base da página
    flexDirection: 'column',
    backgroundColor: '#FFFFFF',
    padding: 40,
    fontSize: 10,
    lineHeight: 1.5,
    fontFamily: 'Helvetica', // Fonte padrão para consistência
  },
  viewer: {
    width: '100%',
    height: '90vh',
  },
  header: {
    paddingBottom: 15,
    borderBottomWidth: 2, // Linha mais grossa
    borderBottomColor: '#333333', // Cinza escuro
    textAlign: 'center',
    marginBottom: 30, // Mais espaço após o cabeçalho
  },
  title: {
    fontSize: 18, // Maior
    fontWeight: 'bold',
    color: '#1A202C', // Quase preto
    marginBottom: 8,
    textTransform: 'uppercase',
  },
  subtitle: {
    fontSize: 12,
    color: '#4A5568', // Cinza escuro
  },
  section: {
    marginBottom: 25, // Aumentar margem entre seções
  },
  sectionTitle: {
    fontSize: 14, // Ligeiramente maior
    fontWeight: 'bold',
    marginBottom: 10,
    color: '#2D3748', // Azul acinzentado escuro
    paddingBottom: 3,
    borderBottomWidth: 1,
    borderBottomColor: '#CBD5E0', // Cinza claro para a linha
    textTransform: 'uppercase',
  },
  subSection: {
    marginBottom: 15,
    paddingLeft: 10, // Recuo para subseções
  },
  subSectionTitle: {
    fontSize: 11,
    fontWeight: 'bold',
    marginBottom: 6,
    color: '#4A5568', // Cinza escuro
  },
  row: {
    flexDirection: 'row',
    marginBottom: 5, // Espaçamento entre linhas de dados
  },
  column: {
    flexDirection: 'column',
    flex: 1,
    paddingRight: 10, // Espaço entre colunas
  },
  label: {
    fontWeight: 'bold',
    width: '35%', // Ajustado
    color: '#718096', // Cinza médio
    marginRight: 5,
  },
  value: {
    width: '65%', // Ajustado
    color: '#2D3748', // Cor mais escura para os valores
  },
  paragraph: {
    marginBottom: 12,
    textAlign: 'justify',
    lineHeight: 1.6, // Melhorar espaçamento entre linhas do parágrafo
  },
  listItem: {
    flexDirection: 'row',
    marginBottom: 5,
    paddingLeft: 10,
  },
  bullet: {
    width: 10,
    fontSize: 10, // Tamanho do bullet
    marginRight: 5,
  },
  listText: { // Não estava sendo usado, removido ou integrar se necessário
    flex: 1,
  },
  cidContainer: {
    marginBottom: 6,
    paddingLeft: 15, // Maior recuo para CIDs
  },
  cidCode: {
    fontWeight: 'bold',
    marginRight: 4,
    color: '#1A202C',
  },
  instrumentCard: { // Card para cada instrumento
    borderWidth: 1,
    borderColor: '#E2E8F0', // Borda cinza clara
    borderRadius: 3,
    paddingHorizontal: 8,
    paddingVertical: 8,
    marginBottom: 10,
    backgroundColor: '#F9FAFB', // Fundo muito sutil
  },
  instrumentHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 6,
  },
  instrumentTitle: {
    fontWeight: 'bold',
    fontSize: 11,
    color: '#374151', // Cinza mais escuro
    flex: 1, // Para ocupar espaço e empurrar a data
  },
  instrumentDate: {
    color: '#6B7280', // Cinza médio
    fontSize: 9,
  },
  referencesSection: {
    marginTop: 25,
    paddingTop: 10,
    borderTopWidth: 0.5,
    borderTopColor: '#D1D5DB', // Cinza um pouco mais escuro
  },
  referencesTitle: {
    fontSize: 11,
    fontWeight: 'bold',
    marginBottom: 8,
    color: '#1A202C', // Quase preto
  },
  referenceItem: {
    marginBottom: 4,
    fontSize: 8,
    lineHeight: 1.4, // Melhorar espaçamento entre linhas
    textAlign: 'justify',
  },
  footer: {
    position: 'absolute',
    bottom: 20,
    left: 40,
    right: 40,
    textAlign: 'center',
    color: '#718096',
    fontSize: 8,
  },
  qrCodeImage: {
    width: 80, // Ajuste o tamanho conforme necessário
    height: 80,
    // alignSelf: 'flex-end', // Removido para permitir a centralização pelo View pai
    marginTop: 20,
  }
});

const LaudoPDFDocument: FC<LaudoPDFDocumentProps> = ({ laudoApiData, qrCodeBase64 }) => {
  if (!laudoApiData) {
    return (
      <Document>
        <Page style={styles.page}>
          <Text>Carregando dados do laudo...</Text>
        </Page>
      </Document>
    );
  }
  // Usa qrCodeBase64 diretamente da prop
  const { laudo_info, paciente_info, avaliacao_info, questionarios_aplicados, todas_referencias_bibliograficas } = laudoApiData;

  const formatarData = (dataString: string | null | undefined) => {
    if (!dataString) return 'Não informada';
    try {
      const data = new Date(dataString);
      // Adiciona fuso horário UTC para consistência
      return data.toLocaleDateString('pt-BR', { timeZone: 'UTC' });
    } catch (e) {
      return dataString;
    }
  };

  const formatarCPF = (cpf: string | null | undefined) => {
    if (!cpf) return 'Não informado';
    return cpf.replace(/(\d{3})(\d{3})(\d{3})(\d{2})/, '$1.$2.$3-$4');
  };
  const renderText = (text: string | null | undefined, fallback = 'Não informado.') => text || fallback;

  return (
    <Document title={`Laudo - ${paciente_info?.nome || 'Paciente'}`}>
      <Page size="A4" style={styles.page}>
        {/* Cabeçalho */}
        <View style={styles.header}>
          <Text style={styles.title}>LAUDO PSICOLÓGICO / NEUROPSICOLÓGICO</Text>
          <Text style={styles.subtitle}>Documento confidencial - Uso profissional</Text>
        </View>

        {/* Dados do Paciente */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Identificação do Paciente</Text>
          
          <View style={styles.row}>
            <View style={styles.column}>
              <View style={styles.row}>
                <Text style={styles.label}>Nome Completo:</Text>
                <Text style={styles.value}>{renderText(paciente_info?.nome)}</Text>
              </View>
              <View style={styles.row}>
                <Text style={styles.label}>Data de Nascimento:</Text>
                <Text style={styles.value}>{formatarData(renderText(paciente_info?.data_nascimento))}</Text>
              </View>
            </View>
            <View style={styles.column}>
              <View style={styles.row}>
                <Text style={styles.label}>CPF:</Text>
                <Text style={styles.value}>{formatarCPF(renderText(paciente_info?.cpf))}</Text>
              </View>
              <View style={styles.row}>
                <Text style={styles.label}>Telefone:</Text>
                <Text style={styles.value}>{paciente_info?.telefone || 'Não informado'}</Text>
              </View>
            </View>
          </View>
        </View>

        {/* Informações da Avaliação */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Informações da Avaliação</Text>
          
          <View style={styles.row}>
            <View style={styles.column}>
              <View style={styles.row}>
                <Text style={styles.label}>Início da Avaliação:</Text>
                <Text style={styles.value}>{formatarData(renderText(avaliacao_info?.data_inicio))}</Text>
              </View>
              <View style={styles.row}>
                <Text style={styles.label}>Unidade de Saúde:</Text>
                <Text style={styles.value}>{renderText(avaliacao_info?.unidade_saude?.nome)}</Text>
              </View>
            </View>
            <View style={styles.column}>
              <View style={styles.row}>
                <Text style={styles.label}>Profissional Responsável:</Text>
                <Text style={styles.value}>{renderText(laudo_info?.medico?.nome)}</Text>
              </View>
              <View style={styles.row}>
                <Text style={styles.label}>Registro/Especialidade:</Text>
                <Text style={styles.value}>
                  {renderText(laudo_info?.medico?.crm, '')}
                  {laudo_info?.medico?.especialidade ? ` - ${laudo_info.medico.especialidade}` : ''}
                </Text>
              </View>
            </View>
          </View>
        </View>

        {/* Dados do Laudo */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Laudo</Text>
          
          <View style={styles.row}>
            <Text style={styles.label}>Data de Emissão do Laudo:</Text>
            <Text style={styles.value}>{formatarData(renderText(laudo_info?.data_emissao))}</Text>
          </View>
          
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>Parecer Diagnóstico / Descrição</Text>
            <Text style={styles.paragraph}>{renderText(laudo_info?.parecer)}</Text>
          </View>
          
          <View style={styles.subSection}>
            <Text style={styles.subSectionTitle}>Abordagem Terapêutica / Encaminhamentos</Text>
            <Text style={styles.paragraph}>{renderText(laudo_info?.abordagem_terapeutica)}</Text>
          </View>
          
          {laudo_info?.cids_associados && laudo_info.cids_associados.length > 0 && (
            <View style={styles.subSection}>
              <Text style={styles.subSectionTitle}>Hipóteses Diagnósticas (CID)</Text>
              {laudo_info.cids_associados.map(cid => (
                <View key={cid.cid} style={styles.cidContainer}>
                  <Text>
                    <Text style={styles.cidCode}>{cid.cid}:</Text> 
                    {cid.descricao}
                  </Text>
                </View>
              ))}
            </View>
          )}
        </View>
        
        {/* Questionários Aplicados */}
        {questionarios_aplicados && questionarios_aplicados.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Instrumentos e Testes Aplicados</Text>
            
            {questionarios_aplicados.map(q => (
              <View key={q.questionario_id} style={styles.instrumentCard}>
                <View style={styles.instrumentHeader}>
                  <Text style={styles.instrumentTitle}>{q.titulo}</Text>
                  {q.data_aplicacao && (
                    <Text style={styles.instrumentDate}>
                      Aplicado em: {formatarData(q.data_aplicacao)}
                    </Text>
                  )}
                </View>
                {q.score !== null && q.score !== undefined && (
                  <Text>
                    <Text style={styles.label}>Pontuação: </Text>
                    {q.score}
                  </Text>
                )}
              </View>
            ))}
          </View>
        )}
        
        {/* Referências Bibliográficas */}
        {todas_referencias_bibliograficas && todas_referencias_bibliograficas.length > 0 && (
          <View style={styles.referencesSection}>
            <Text style={styles.referencesTitle}>Referências Bibliográficas</Text>
            
            {todas_referencias_bibliograficas.map((ref, index) => (
              <View key={index} style={styles.listItem}>
                <Text style={styles.bullet}>• </Text>
                <Text style={styles.referenceItem}>{ref}</Text>
              </View>
            ))}
          </View>
        )}

        {/* QR Code da Assinatura */}
        {qrCodeBase64 && ( // Verifica a prop qrCodeBase64
          <View style={{
            ...styles.section, // Mantém os estilos da seção
            alignItems: 'center', // Centraliza os itens filhos horizontalmente
            width: '100%' // Garante que o View ocupe toda a largura disponível
          }}>
            <Image style={styles.qrCodeImage} src={qrCodeBase64} />
            <Text style={{ 
              fontSize: 9, // Tamanho menor
              textAlign: 'center', // Centralizado
              marginTop: 5 // Pequena margem para separar do QR code
            }}>Assinatura do Profissional Responsável</Text>
          </View>
        )}

        {/* Rodapé */}
        <Text style={styles.footer}>
          Documento gerado eletronicamente em {new Date().toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit', year: 'numeric' })} |
          Sistema NeuroGAP | Confidencial
        </Text>
      </Page>
    </Document>
  );
};

const LaudoPDFViewer: FC<LaudoPDFViewerProps> = ({ avaliacaoId }) => {
  const [laudoData, setLaudoData] = useState<LaudoApiData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [qrCodeBase64, setQrCodeBase64] = useState<string | null>(null);

  useEffect(() => {

    
    const fetchLaudoData = async () => {
      try {
        setLoading(true);
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const apiUrl = `${baseUrl}/laudos/avaliacao/${avaliacaoId}/pdf_data`;

        const response = await fetch(apiUrl);
        
        if (!response.ok) {
          throw new Error(`Erro ao carregar dados: ${response.status}`);
        }

        const data = await response.json();
        // Após buscar os dados do laudo, buscar o QR code
        if (data.laudo_info?.medico?.id && data.laudo_info?.data_emissao) {
          const medicoIdParaQr = data.laudo_info.medico.id;
          const timestampParaQr = data.laudo_info.data_emissao;
          console.log("DENTRO DO IF - Dados para QR:", medicoIdParaQr, timestampParaQr);

          try {
            const qrResponse = await fetch(`${baseUrl}/laudos/gerar_qr_assinatura`, {
              method: 'POST',
              headers: {
                'Content-Type': 'application/json',
                // Adicione token de autorização se a rota /gerar_qr_assinatura for protegida
                 'Authorization': `Bearer ${localStorage.getItem("@App:token")}`, // DESCOMENTE ESTA LINHA
              },
              body: JSON.stringify({
                medico_id: medicoIdParaQr,
                timestamp_assinatura: timestampParaQr,
              }),
            });
            if (qrResponse.ok) {
              const qrData = await qrResponse.json();
              console.log("QR code gerado:", qrData.qr_code_base64);
              setQrCodeBase64(qrData.qr_code_base64);
            } else {
              const errorText = await qrResponse.text();
              console.error(`Erro ao gerar QR code da assinatura (${qrResponse.status}):`, errorText);
              setError(`Falha ao gerar QR code: ${errorText}`); // Atualiza o estado de erro
            }
          } catch (qrErr) {
            console.error("Erro de EXCEÇÃO ao gerar QR code:", qrErr);
            setError(qrErr instanceof Error ? `Exceção ao gerar QR: ${qrErr.message}` : 'Exceção desconhecida ao gerar QR');
          }
        }
        setLaudoData(data);
        setError(null);
      } catch (err) {
        console.error("Erro ao buscar dados do laudo:", err);
        setError(err instanceof Error ? err.message : 'Erro desconhecido');
        setLaudoData(null);
      } finally {
        setLoading(false);
      }
    };

    if (avaliacaoId) {

      fetchLaudoData();
    } else {
      setLoading(false); // Garante que o loading pare se não houver ID
      setError("ID da avaliação não fornecido para carregar o laudo."); // Informa o usuário
    }
  }, [avaliacaoId]);

  if (loading) {
    return <div style={{ padding: '20px' }}>Carregando prévia do laudo...</div>;
  }

  if (error) {
    return <div style={{ color: 'red', padding: '20px' }}>Erro: {error}</div>;
  }

  if (!laudoData) {
    return <div style={{ padding: '20px' }}>Nenhum dado disponível para exibir</div>;
  }

 return (
    <div style={{ height: '100vh' }}>
      <PDFViewer style={styles.viewer}>
        <LaudoPDFDocument laudoApiData={laudoData} qrCodeBase64={qrCodeBase64} />
      </PDFViewer>
    </div>
  );
};

export default LaudoPDFViewer;