export type AppRole =
  | "rol_admin"
  | "rol_gerente"
  | "rol_vendedor"
  | "rol_bodeguero"
  | "rol_auditor"

export const routeRoles = {
  home: ["rol_admin", "rol_gerente", "rol_vendedor", "rol_bodeguero", "rol_auditor"],
  inventario: ["rol_admin", "rol_gerente", "rol_vendedor", "rol_bodeguero", "rol_auditor"],
  proveedores: ["rol_admin", "rol_gerente", "rol_bodeguero", "rol_auditor"],
  categorias: ["rol_admin", "rol_gerente", "rol_bodeguero", "rol_auditor"],
  ventas: ["rol_admin", "rol_gerente", "rol_vendedor", "rol_auditor"],
  clientes: ["rol_admin", "rol_gerente", "rol_vendedor", "rol_auditor"],
  empleados: ["rol_admin", "rol_gerente", "rol_auditor"],
} satisfies Record<string, AppRole[]>

export function canAccess(role: string | undefined, allowedRoles: AppRole[]) {
  return Boolean(role && allowedRoles.includes(role as AppRole))
}