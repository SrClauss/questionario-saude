import AdminLayout from '../layouts/AdminLayout'
import StylizedTitle from '../components/StylizedTitle'
import { auth } from '../utils/auth'

export default function AdminHomeScreen() {

    return (
        <AdminLayout>
            <StylizedTitle title="Home" />
            <div>{JSON.stringify(auth.getToken())}</div>
            <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', height: '50vh' }}>
                <h1>Bem-vindo ao sistema de gerenciamento de questionários!</h1>
                <p>Selecione uma opção no menu lateral para começar.</p>
            </div>
        </AdminLayout>
    )
}