import { Gender, createPerson } from "@/data/person";
import { z } from "zod";

export async function POST(request: Request) {
  const schema = z
    .object({
      motherId: z.string().nullable(),
      fatherId: z.string().nullable(),
      firstName: z.string(),
      lastName: z.string(),
    })
    .strict();

  const json = await request.json().catch(() => null);
  const result = await schema.safeParseAsync(json);

  return result.success
    ? Response.json(await createPerson(Gender.Male, result.data), {
        status: 201,
      })
    : Response.json(result.error, { status: 400 });
}
