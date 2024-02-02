import { Gender, deletePerson, getPerson } from "@/data/person";

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const person = await getPerson(Gender.Male, params.id);

  return person !== null
    ? Response.json(person)
    : new Response(null, { status: 404 });
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const deleted = await deletePerson(Gender.Male, params.id);

  return new Response(null, { status: deleted ? 204 : 404 });
}
