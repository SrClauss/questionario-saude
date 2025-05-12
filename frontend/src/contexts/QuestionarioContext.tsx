import React, { createContext, useState, useContext } from 'react';

interface QuestionarioContextProps {
  hasBaterias: boolean;
  setHasBaterias: (value: boolean) => void;
}

const QuestionarioContext = createContext<QuestionarioContextProps>({
  hasBaterias: false,
  setHasBaterias: () => {}
});

export const QuestionarioProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [hasBaterias, setHasBaterias] = useState<boolean>(false);
  return (
    <QuestionarioContext.Provider value={{ hasBaterias, setHasBaterias }}>
      {children}
    </QuestionarioContext.Provider>
  );
};

export const useQuestionarioContext = () => useContext(QuestionarioContext);