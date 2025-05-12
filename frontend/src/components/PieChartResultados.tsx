import React from 'react';
import { PieChart, Pie, Cell } from 'recharts';
import { Typography, Box } from '@mui/material';

interface PieChartResultadosProps {
  respostas: any[];
  qtd_perguntas: number;
}

const COLORS = ['#0088FE', '#FF8042'];

const PieChartResultados: React.FC<PieChartResultadosProps> = ({ respostas, qtd_perguntas }) => {
  const responded = respostas.length;
  const notResponded = qtd_perguntas - responded;
  const total = responded + notResponded;
  const percentage = total > 0 ? Math.round((responded / total) * 100) : 0;

  const data = [
    { name: 'Respondidas', value: responded },
    { name: 'Não respondidas', value: notResponded },
  ];

  return (
    <Box sx={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <PieChart width={200} height={200}>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          innerRadius="60%"
          outerRadius="80%"
          fill="#8884d8"
          dataKey="value"
          label={false}
        >
          {data.map((_entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
      </PieChart>
      <Typography variant="h6" >
        A avaliação está em: {percentage}%
      </Typography>
    </Box>
  );
};

export default PieChartResultados;