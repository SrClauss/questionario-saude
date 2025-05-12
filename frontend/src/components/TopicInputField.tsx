import React, { useState, useCallback } from 'react';
import { TextField, Box, IconButton, List, ListItem, ListItemText } from '@mui/material';
import { Delete as DeleteIcon } from '@mui/icons-material';

interface TopicInputFieldProps {
  initialTopics?: string[];
  onChange: (topics: string[]) => void;
}

const TopicInputField: React.FC<TopicInputFieldProps> = ({ initialTopics = [], onChange }) => {
  const [topics, setTopics] = useState<string[]>(initialTopics);
  const [newTopic, setNewTopic] = useState('');

  const handleAddTopic = useCallback(() => {
    if (newTopic.trim() !== '') {
      const updatedTopics = [...topics, newTopic.trim()];
      setTopics(updatedTopics);
      onChange(updatedTopics);
      setNewTopic('');
    }
  }, [newTopic, topics, onChange]);

  const handleRemoveTopic = useCallback((indexToRemove: number) => {
    const updatedTopics = topics.filter((_, index) => index !== indexToRemove);
    setTopics(updatedTopics);
    onChange(updatedTopics);
  }, [topics, onChange]);

  const handleKeyDown = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter') {
      handleAddTopic();
    }
  };

  return (
    <Box>
      <TextField
        label="Adicionar Tópico"
        variant="outlined"
        fullWidth
        margin="normal"
        size='small'
        value={newTopic}
        onChange={(e) => setNewTopic(e.target.value)}
        onKeyDown={handleKeyDown}
        placeholder="Pressione Enter para adicionar"
      />

      <List>
        {topics.map((topic, index) => (
          <ListItem key={index} secondaryAction={
            <IconButton edge="end" aria-label="delete" onClick={() => handleRemoveTopic(index)}>
              <DeleteIcon />
            </IconButton>
          }>
            <ListItemText primary={topic} />
          </ListItem>
        ))}
      </List>
    </Box>
  );
};

export default TopicInputField;