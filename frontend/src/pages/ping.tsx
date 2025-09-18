import { useQuery } from '@tanstack/react-query';

export default function Ping() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['health'],
    queryFn: async () => {
      const res = await fetch('/api/healthz');
      if (!res.ok) throw new Error('Network response was not ok');
      return res.json() as Promise<{ status: string }>;
    },
  });

  if (isLoading) return <p>Loading...</p>;
  if (error) return <p>Error: {(error as Error).message}</p>;

  return (
    <div className="flex flex-col items-center justify-center h-screen">
      <h1 className="text-3xl font-bold">Backend Health</h1>
      <p className="mt-4 text-xl text-green-600">{data?.status}</p>
    </div>
  );
}
