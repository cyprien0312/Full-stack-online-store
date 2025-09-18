import type { UserList, User } from '@/types/users';

export async function getUsers(
  params: {
    page?: number;
    size?: number;
    q?: string;
    sort?: 'id' | 'email' | 'name' | 'created_at';
    order?: 'asc' | 'desc';
  } = {}
): Promise<UserList> {
  const qs = new URLSearchParams();
  if (params.page) qs.set('page', String(params.page));
  if (params.size) qs.set('size', String(params.size));
  if (params.q) qs.set('q', params.q);
  if (params.sort) qs.set('sort', params.sort);
  if (params.order) qs.set('order', params.order);

  const url = `/api/users/${qs.toString() ? `?${qs.toString()}` : ''}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error(`Request failed: ${res.status}`);
  return res.json();
}

export async function createUser(body: { email: string; name: string }): Promise<User> {
  const res = await fetch('/api/users/', {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Create failed: ${res.status}`);
  return res.json();
}

export async function updateUser(
  id: number,
  body: Partial<{ email: string; name: string }>
): Promise<User> {
  const res = await fetch(`/api/users/${id}`, {
    method: 'PATCH',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(body),
  });
  if (!res.ok) throw new Error(`Update failed: ${res.status}`);
  return res.json();
}

export async function deleteUser(id: number): Promise<void> {
  const res = await fetch(`/api/users/${id}`, { method: 'DELETE' });
  if (!res.ok) throw new Error(`Delete failed: ${res.status}`);
}
