import React from 'react';
import { Link } from 'wouter';
import { MoonIcon, SunIcon } from 'lucide-react';
import { useTheme } from '@/components/ui/theme-provider';
import { Button } from '@/components/ui/button';

const Header = () => {
  const { theme, setTheme } = useTheme();

  return (
    <header className="bg-background border-b sticky top-0 z-10">
      <div className="container mx-auto px-4 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <Link href="/">
            <a className="font-bold text-xl bg-gradient-to-r from-indigo-500 via-purple-500 to-pink-500 bg-clip-text text-transparent">
              TrueAlphaSpiral
            </a>
          </Link>
        </div>
        
        <nav className="hidden md:flex items-center gap-4">
          <Link href="/">
            <a className="text-sm font-medium hover:text-primary transition-colors">
              Home
            </a>
          </Link>
          <Link href="#verify">
            <a className="text-sm font-medium hover:text-primary transition-colors">
              Verify Content
            </a>
          </Link>
          <Link href="/about">
            <a className="text-sm font-medium hover:text-primary transition-colors">
              About
            </a>
          </Link>
          <Link href="/documentation">
            <a className="text-sm font-medium hover:text-primary transition-colors">
              Documentation
            </a>
          </Link>
        </nav>
        
        <div className="flex items-center gap-2">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
            title={theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'}
          >
            {theme === 'dark' ? <SunIcon className="h-[1.2rem] w-[1.2rem]" /> : <MoonIcon className="h-[1.2rem] w-[1.2rem]" />}
            <span className="sr-only">Toggle theme</span>
          </Button>
        </div>
      </div>
    </header>
  );
};

export default Header;