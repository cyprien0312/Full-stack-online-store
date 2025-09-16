import type { UserList } from '@/types/users';

export async function getUsers(params: {
  page?: number;
  size?: number;
  q?: string;
  sort?: 'id' | 'email' | 'name' | 'created_at';
  order?: 'asc' | 'desc';
} = {}): Promise<UserList> {
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