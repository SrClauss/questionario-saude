import React from 'react';
import { PieChart, Pie, Cell } from 'recharts';
import { Typography, Box, useTheme } from '@mui/material';

interface PieChartResultadosProps {
  respostas: {};
  qtd_perguntas: number;
  mode?: 'normal' | 'tiny';
}

const COLORS = ['#0088FE', '#FF8042'];

const PieChartResultados: React.FC<PieChartResultadosProps> = ({ respostas, qtd_perguntas, mode = 'normal' }) => {
  const responded = Object.keys(respostas).length;
  const notResponded = qtd_perguntas - responded;
  const total = responded + notResponded;
  const percentage = total > 0 ? Math.round((responded / total) * 100) : 0;
  const theme = useTheme();

  const data = [
    { name: 'Respondidas', value: responded },
    { name: 'Não respondidas', value: notResponded },
  ];

  const chartSize = mode === 'normal' ? 200 : 100;
  const fontSize = mode === 'normal' ? 'h6' : 'body2';
  const percentageSize = mode === 'normal' ? 'h1' : 'h4';

  return (
    <Box sx={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
      <PieChart width={chartSize} height={chartSize}>
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

      {
        mode === 'normal' && (
          <Typography variant={fontSize} >
            A avaliação está em:
          </Typography>
        )


      }
      <Typography variant={percentageSize} sx={{ fontWeight: 'bold', color: theme.palette.info.main }}>
        {percentage}%
      </Typography>
    </Box>
  );
};

export default PieChartResultados;