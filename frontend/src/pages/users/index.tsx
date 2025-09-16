import { useState, useMemo } from 'react';
import { keepPreviousData, useQuery } from '@tanstack/react-query';
import { getUsers } from '@/lib/api';
import type { User, UserList } from '@/types/users';

export default function UsersPage() {
  const [page, setPage] = useState(1);
  const [size, setSize] = useState(10);
  const [q, setQ] = useState('');
  const [sort, setSort] = useState<'id' | 'email' | 'name' | 'created_at'>('id');
  const [order, setOrder] = useState<'asc' | 'desc'>('asc');

  const queryKey = useMemo(() => ['users', { page, size, q, sort, order }], [page, size, q, sort, order]);

  const { data, isLoading, isFetching, error } = useQuery<UserList>({
    queryKey,
    queryFn: () => getUsers({ page, size, q: q.trim() || undefined, sort, order }),
    placeholderData: keepPreviousData,
  });

  const items = data?.items ?? [];
  const total = data?.total ?? 0;
  const totalPages = Math.max(1, Math.ceil(total / size));

  const toggleSort = (key: 'id' | 'email' | 'name' | 'created_at') => {
    if (sort === key) setOrder(order === 'asc' ? 'desc' : 'asc');
    else {
      setSort(key);
      setOrder('asc');
    }
    setPage(1);
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold">Users</h1>

      <div className="mt-4 flex gap-3 items-center">
        <input
          className="border rounded px-3 py-1"
          placeholder="Search email or name"
          value={q}
          onChange={(e) => { setQ(e.target.value); setPage(1); }}
        />
        <select
          className="border rounded px-2 py-1"
          value={size}
          onChange={(e) => { setSize(Number(e.target.value)); setPage(1); }}
        >
          {[5,10,20,50].map(s => <option key={s} value={s}>{s}/page</option>)}
        </select>
        {isFetching && <span className="text-sm text-gray-500">Refreshing…</span>}
      </div>

      {isLoading ? (
        <p className="mt-6">Loading…</p>
      ) : error ? (
        <p className="mt-6 text-red-600">Error: {(error as Error).message}</p>
      ) : (
        <>
          <table className="mt-4 w-full border-collapse">
            <thead>
              <tr className="text-left border-b">
                <th className="py-2 cursor-pointer" onClick={() => toggleSort('id')}>ID {sort==='id' ? (order==='asc'?'▲':'▼') : ''}</th>
                <th className="py-2 cursor-pointer" onClick={() => toggleSort('email')}>Email {sort==='email' ? (order==='asc'?'▲':'▼') : ''}</th>
                <th className="py-2 cursor-pointer" onClick={() => toggleSort('name')}>Name {sort==='name' ? (order==='asc'?'▲':'▼') : ''}</th>
              </tr>
            </thead>
            <tbody>
              {items.map((u: User) => (
                <tr key={u.id} className="border-b">
                  <td className="py-2">{u.id}</td>
                  <td className="py-2">{u.email}</td>
                  <td className="py-2">{u.name}</td>
                </tr>
              ))}
              {items.length === 0 && (
                <tr><td className="py-4 text-gray-500" colSpan={3}>No data</td></tr>
              )}
            </tbody>
          </table>

          <div className="mt-4 flex items-center gap-3">
            <button
              className="border rounded px-3 py-1 disabled:opacity-50"
              onClick={() => setPage((p) => Math.max(1, p - 1))}
              disabled={page <= 1}
            >
              Prev
            </button>
            <span>Page {page} / {totalPages} (Total {total})</span>
            <button
              className="border rounded px-3 py-1 disabled:opacity-50"
              onClick={() => setPage((p) => Math.min(totalPages, p + 1))}
              disabled={page >= totalPages}
            >
              Next
            </button>
          </div>
        </>
      )}
    </div>
  );
}