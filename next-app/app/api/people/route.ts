import prisma from "@/db";
import { z } from "zod";

export async function GET(request: Request) {
  const people = await prisma.person.findMany({
    include: { male: true, female: true },
  });

  return Response.json(
    people.map((person) => {
      const x = person.male ?? person.female;

      if (x === null) throw new Error("Person has no gender");

      return {
        ...x,
        gender: x === person.male ? "male" : "female",
        firstName: person.firstName,
        lastName: person.lastName,
      };
    })
  );
}

export async function POST(request: Request) {
  const schema = z.object({
    gender: z.enum(["male", "female"]),
    motherId: z.string().nullish(),
    fatherId: z.string().nullish(),
    firstName: z.string(),
    lastName: z.string(),
  });

  const json = await request.json().catch(() => null);
  const result = await schema.safeParseAsync(json);

  if (result.success) {
    const { gender, motherId, fatherId, firstName, lastName } = result.data;
    const person =
      gender === "male"
        ? await prisma.male.create({
            data: {
              father: fatherId ? { connect: { id: fatherId } } : undefined,
              mother: motherId ? { connect: { id: motherId } } : undefined,
              person: { create: { firstName, lastName } },
            },
          })
        : await prisma.female.create({
            data: {
              father: fatherId ? { connect: { id: fatherId } } : undefined,
              mother: motherId ? { connect: { id: motherId } } : undefined,
              person: { create: { firstName, lastName } },
            },
          });

    return Response.json(person, { status: 201 });
  }
  return Response.json(result.error, { status: 400 });
}
