import prisma from "@/db";

export enum Gender {
  Male,
  Female,
}

export interface Person {
  id: string;
  motherId: string | null;
  fatherId: string | null;
  firstName: string;
  lastName: string;
}

export async function getPerson(
  gender: Gender,
  id: string
): Promise<Person | null> {
  type MaleArgs = Parameters<typeof prisma.male.findUnique>[0];
  type FemaleArgs = Parameters<typeof prisma.female.findUnique>[0];

  const args = {
    where: { id },
    select: {
      motherId: true,
      fatherId: true,
      person: {
        select: { firstName: true, lastName: true },
      },
    },
  } satisfies MaleArgs & FemaleArgs;
  const person = await (gender === Gender.Male
    ? prisma.male.findUnique(args)
    : prisma.female.findUnique(args));

  if (person !== null) {
    const {
      fatherId,
      motherId,
      person: { firstName, lastName },
    } = person;

    return { id, fatherId, motherId, firstName, lastName };
  }
  return null;
}

export async function deletePerson(
  gender: Gender,
  id: string
): Promise<boolean> {
  type MaleArgs = Parameters<typeof prisma.male.delete>[0];
  type FemaleArgs = Parameters<typeof prisma.female.delete>[0];

  const args = {
    where: { id },
  } satisfies MaleArgs & FemaleArgs;
  const deleted = await (gender === Gender.Male
    ? prisma.male.delete(args)
    : prisma.female.delete(args)
  )
    .then(() => prisma.person.delete(args))
    .catch(() => null);

  return deleted !== null;
}
