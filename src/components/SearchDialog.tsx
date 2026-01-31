import { useEffect, useState, useCallback } from 'react';
import { Command } from 'cmdk';

interface SearchItem {
  title: string;
  href: string;
  type: 'page' | 'blog' | 'note';
}

interface SearchDialogProps {
  items: SearchItem[];
}

export default function SearchDialog({ items }: SearchDialogProps) {
  const [open, setOpen] = useState(false);
  const [search, setSearch] = useState('');

  // Toggle the menu when Cmd+K is pressed
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        setOpen((prev) => !prev);
      }
      if (e.key === 'Escape') {
        setOpen(false);
      }
    };

    document.addEventListener('keydown', handleKeyDown);

    // Listen for custom event from header
    const handleOpenSearch = () => setOpen(true);
    document.addEventListener('open-search', handleOpenSearch);

    return () => {
      document.removeEventListener('keydown', handleKeyDown);
      document.removeEventListener('open-search', handleOpenSearch);
    };
  }, []);

  const handleSelect = useCallback((href: string) => {
    setOpen(false);
    window.location.href = href;
  }, []);

  // Filter items based on search
  const filteredItems = items.filter((item) =>
    item.title.toLowerCase().includes(search.toLowerCase())
  );

  // Group items by type
  const pages = filteredItems.filter((item) => item.type === 'page');
  const blogs = filteredItems.filter((item) => item.type === 'blog');
  const notes = filteredItems.filter((item) => item.type === 'note');

  if (!open) return null;

  return (
    <div className="fixed inset-0 z-50">
      {/* Backdrop */}
      <div
        className="fixed inset-0 bg-black/50 backdrop-blur-sm"
        onClick={() => setOpen(false)}
      />

      {/* Dialog */}
      <div className="fixed left-1/2 top-1/4 w-full max-w-lg -translate-x-1/2 -translate-y-1/4 p-4">
        <Command
          className="rounded-xl border border-[#27272a] bg-[#0a0a0a] shadow-2xl overflow-hidden"
          loop
        >
          <div className="flex items-center border-b border-[#27272a] px-4">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              className="h-5 w-5 text-[#71717a] mr-3"
              fill="none"
              viewBox="0 0 24 24"
              stroke="currentColor"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
              />
            </svg>
            <Command.Input
              value={search}
              onValueChange={setSearch}
              placeholder="Search..."
              className="flex-1 bg-transparent py-4 text-[#fafafa] placeholder-[#71717a] outline-none"
            />
            <kbd className="hidden sm:inline-flex items-center gap-1 rounded bg-[#141414] px-2 py-1 text-xs text-[#71717a]">
              ESC
            </kbd>
          </div>

          <Command.List className="max-h-80 overflow-y-auto p-2">
            <Command.Empty className="py-6 text-center text-sm text-[#71717a]">
              No results found.
            </Command.Empty>

            {pages.length > 0 && (
              <Command.Group
                heading="Pages"
                className="text-xs font-medium text-[#71717a] px-2 py-1.5"
              >
                {pages.map((item) => (
                  <Command.Item
                    key={item.href}
                    value={item.title}
                    onSelect={() => handleSelect(item.href)}
                    className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-[#a1a1aa] cursor-pointer data-[selected=true]:bg-[#141414] data-[selected=true]:text-[#fafafa]"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-4 w-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                      />
                    </svg>
                    {item.title}
                  </Command.Item>
                ))}
              </Command.Group>
            )}

            {blogs.length > 0 && (
              <Command.Group
                heading="Blog Posts"
                className="text-xs font-medium text-[#71717a] px-2 py-1.5 mt-2"
              >
                {blogs.slice(0, 10).map((item) => (
                  <Command.Item
                    key={item.href}
                    value={item.title}
                    onSelect={() => handleSelect(item.href)}
                    className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-[#a1a1aa] cursor-pointer data-[selected=true]:bg-[#141414] data-[selected=true]:text-[#fafafa]"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-4 w-4"
                      fill="none"
                      viewBox="0 0 24 24"
                      stroke="currentColor"
                    >
                      <path
                        strokeLinecap="round"
                        strokeLinejoin="round"
                        strokeWidth={2}
                        d="M19 20H5a2 2 0 01-2-2V6a2 2 0 012-2h10a2 2 0 012 2v1m2 13a2 2 0 01-2-2V7m2 13a2 2 0 002-2V9a2 2 0 00-2-2h-2m-4-3H9M7 16h6M7 8h6v4H7V8z"
                      />
                    </svg>
                    {item.title}
                  </Command.Item>
                ))}
                {blogs.length > 10 && (
                  <div className="px-3 py-2 text-xs text-[#71717a]">
                    + {blogs.length - 10} more posts
                  </div>
                )}
              </Command.Group>
            )}

            {notes.length > 0 && (
              <Command.Group
                heading="Notes"
                className="text-xs font-medium text-[#71717a] px-2 py-1.5 mt-2"
              >
                {notes.slice(0, 5).map((item) => (
                  <Command.Item
                    key={item.href}
                    value={item.title}
                    onSelect={() => handleSelect(item.href)}
                    className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-[#a1a1aa] cursor-pointer data-[selected=true]:bg-[#141414] data-[selected=true]:text-[#fafafa]"
                  >
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-4 w-4"
                      fill="currentColor"
                      viewBox="0 0 24 24"
                    >
                      <path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z" />
                    </svg>
                    <span className="truncate">{item.title}</span>
                  </Command.Item>
                ))}
                {notes.length > 5 && (
                  <Command.Item
                    value="view-all-notes"
                    onSelect={() => handleSelect('/notes/')}
                    className="flex items-center gap-3 rounded-lg px-3 py-2 text-sm text-[#10b981] cursor-pointer data-[selected=true]:bg-[#141414]"
                  >
                    View all {notes.length} notes
                  </Command.Item>
                )}
              </Command.Group>
            )}
          </Command.List>

          <div className="border-t border-[#27272a] px-4 py-2 text-xs text-[#71717a]">
            <span className="flex items-center gap-2">
              <kbd className="rounded bg-[#141414] px-1.5 py-0.5">↑↓</kbd>
              <span>to navigate</span>
              <kbd className="rounded bg-[#141414] px-1.5 py-0.5 ml-2">↵</kbd>
              <span>to select</span>
            </span>
          </div>
        </Command>
      </div>
    </div>
  );
}
