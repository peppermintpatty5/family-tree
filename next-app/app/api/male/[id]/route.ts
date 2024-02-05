import { Gender, deletePerson, getPerson, updatePerson } from "@/data/person";
import { z } from "zod";

export async function GET(
  request: Request,
  { params }: { params: { id: string } }
) {
  const person = await getPerson(Gender.Male, params.id);

  return person !== null
    ? Response.json(person)
    : new Response(null, { status: 404 });
}

export async function PATCH(
  request: Request,
  { params }: { params: { id: string } }
) {
  const schema = z
    .object({
      motherId: z.string().nullable(),
      fatherId: z.string().nullable(),
      firstName: z.string(),
      lastName: z.string(),
    })
    .partial()
    .strict();
  const json = await request.json().catch(() => null);
  const result = await schema.safeParseAsync(json);
  const updated =
    result.success && (await updatePerson(Gender.Male, params.id, result.data));

  return new Response(null, { status: updated ? 204 : 400 });
}

export async function DELETE(
  request: Request,
  { params }: { params: { id: string } }
) {
  const deleted = await deletePerson(Gender.Male, params.id);

  return new Response(null, { status: deleted ? 204 : 400 });
}
