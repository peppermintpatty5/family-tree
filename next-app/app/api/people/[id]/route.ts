import prisma from "@/db";

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const person = await prisma.person.findUnique({ where: { id: params.id } });

  return person !== null
    ? Response.json(person)
    : new Response(null, { status: 404 });
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  // No automatic cascading delete, must delete in male/female tables first
  await prisma.male.delete({ where: { id: params.id } }).catch(() => null);
  await prisma.female.delete({ where: { id: params.id } }).catch(() => null);

  const person = await prisma.person
    .delete({ where: { id: params.id } })
    .catch(() => null);

  return person !== null
    ? new Response(null, { status: 204 })
    : new Response(null, { status: 404 });
}
