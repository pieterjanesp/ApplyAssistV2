import { NavLink } from 'react-router-dom'
import { ROUTES } from '../../config/routes'

const navItems = [
  { label: 'Profile', path: ROUTES.PROFILE },
  { label: 'Generate CV', path: ROUTES.CV_GENERATE },
  { label: 'Optimise CV', path: ROUTES.CV_OPTIMISE },
  { label: 'Jobs', path: ROUTES.JOBS },
  { label: 'Applications', path: ROUTES.APPLICATION_MANAGER },
]

export function Sidebar() {
  return (
    <aside className="flex h-screen w-64 flex-col border-r border-gray-200 bg-white">
      <div className="p-6">
        <h1 className="text-xl font-bold text-gray-900">ApplyAssist</h1>
      </div>
      <nav className="flex-1 space-y-1 px-3">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `block rounded-md px-3 py-2 text-sm font-medium ${
                isActive
                  ? 'bg-blue-50 text-blue-700'
                  : 'text-gray-700 hover:bg-gray-50 hover:text-gray-900'
              }`
            }
          >
            {item.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
