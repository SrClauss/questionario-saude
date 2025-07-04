import { auth } from "../utils/auth";
import AdminLayout from "./AdminLayout";
import MedicoLayout from "./MedicoLayout";
import PacienteLayout from "./PacienteLayout";
import ProfissionalLayout from "./ProfissionalLayout";

export default function VariableLayout({ children }: { children: React.ReactNode }) {

    const user = auth.getUserData()


    if (user?.role === 'admin') {
        return <AdminLayout>{children}</AdminLayout>
    } else if (user?.role === 'profissional_saude') {
        return <ProfissionalLayout>{children}</ProfissionalLayout>
    } else if (user?.role === 'paciente') {
        return <PacienteLayout>{children}</PacienteLayout>
    } else if(user?.role === 'medico'){
        return <MedicoLayout>{children}</MedicoLayout>
    }
    else if(user?.role === 'colaborador'){
        return <ProfissionalLayout>{children}</ProfissionalLayout>
    }
    
    
}