import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface Usuario {
  id: number;
  username: string;
  nombre: string;
  apellido: string;
  rol: 'ADMINISTRADOR' | 'ANALISTA_SENIOR' | 'ANALISTA_JUNIOR' | 'CONSULTA';
}

interface AuthState {
  isAuthenticated: boolean;
  usuario: Usuario | null;
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => void;
  hasPermission: (permission: string) => boolean;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      isAuthenticated: false,
      usuario: null,
      token: null,

      login: async (username: string, password: string) => {
        // TODO: Implementar autenticación real
        // Por ahora, simulamos un login exitoso
        if (username === 'admin' && password === 'admin123') {
          const usuario: Usuario = {
            id: 1,
            username: 'admin',
            nombre: 'Administrador',
            apellido: 'Sistema',
            rol: 'ADMINISTRADOR',
          };

          set({
            isAuthenticated: true,
            usuario,
            token: 'fake-jwt-token',
          });
        } else {
          throw new Error('Credenciales inválidas');
        }
      },

      logout: () => {
        set({
          isAuthenticated: false,
          usuario: null,
          token: null,
        });
      },

      hasPermission: (permission: string) => {
        const { usuario } = get();
        if (!usuario) return false;

        const permissions: Record<string, string[]> = {
          ADMINISTRADOR: ['*'],
          ANALISTA_SENIOR: [
            'crear',
            'editar',
            'eliminar',
            'exportar',
            'consultar',
          ],
          ANALISTA_JUNIOR: ['crear', 'editar_propio', 'consultar'],
          CONSULTA: ['consultar'],
        };

        const userPermissions = permissions[usuario.rol] || [];
        return (
          userPermissions.includes('*') || userPermissions.includes(permission)
        );
      },
    }),
    {
      name: 'signa-auth',
    }
  )
);
