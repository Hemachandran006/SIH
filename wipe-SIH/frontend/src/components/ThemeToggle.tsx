import * as Switch from '@radix-ui/react-switch'
import { Moon, Sun } from 'lucide-react'
import { useTheme } from '../context/ThemeProvider'

export function ThemeToggle() {
  const { theme, toggle } = useTheme()
  const isDark = theme === 'dark'
  return (
    <div className="flex items-center gap-2">
      <Sun size={16} className="opacity-70" />
      <Switch.Root
        className="w-10 h-6 bg-black/10 dark:bg-white/10 rounded-full relative data-[state=checked]:bg-black/20 dark:data-[state=checked]:bg-white/20 transition-colors"
        checked={isDark}
        onCheckedChange={toggle}
      >
        <Switch.Thumb className="block w-5 h-5 bg-white dark:bg-slate-800 rounded-full shadow-soft transition-transform translate-x-0.5 will-change-transform data-[state=checked]:translate-x-[18px]" />
      </Switch.Root>
      <Moon size={16} className="opacity-70" />
    </div>
  )
}