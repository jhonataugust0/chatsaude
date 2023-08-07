import { sleep, check } from 'k6';
import http from 'k6/http';

const headers = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  };

const host = 'http://localhost:8000';

function generate_random_date() {
  const startDate = new Date(2023, 7, 1); // Note: JavaScript months are 0-indexed (0 is January)
  const endDate = new Date(2072, 11, 31);

  const daysDiff = (endDate - startDate) / (1000 * 60 * 60 * 24);

  const randomDays = Math.floor(Math.random() * daysDiff);

  const randomDate = new Date(startDate.getTime() + randomDays * (1000 * 60 * 60 * 24));

  const formattedDate = randomDate.toISOString().split('T')[0];
  console.log(`DATA ${formattedDate}`);
  return formattedDate;
}

function generate_random_time() {
  const startTime = new Date(0, 0, 0, 0, 0, 0);
  const endTime = new Date(0, 0, 0, 23, 59, 59);

  const timeDiff = (endTime - startTime) / 1000;

  const randomSeconds = Math.floor(Math.random() * timeDiff);

  const randomTime = new Date(startTime.getTime() + randomSeconds * 1000);

  const formattedTime = randomTime.toTimeString().split(' ')[0];
  console.log(`TIME ${formattedTime}`);
  return formattedTime;
}


export const options = {
  vus: 5, // Número de usuários virtuais (VUs) simultâneos
  iterations: 5, // Número de iterações por VU
};

// Função para fazer uma requisição POST usando o httpx e retornar o JSON de resposta
function make_post_request(url, payload) {
  const response = http.post(url, JSON.stringify(payload), { headers: headers });
  return JSON.parse(response.body);
}

// Teste: Agendamento de usuário
export function test_register_consult() {
  const payload = {
    "contact": {
      "name": "",
      "urn": "tel:+12065551212",
      "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
    },
    "flow": {
      "name": "fluxo_registro",
      "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
    },
    "results": {
      "message": {
        "category": "message",
        "value": "1"
      }
    }
  };
  const response = make_post_request(`${host}/insert_schedule_consult`, payload);
  check(response.status, { 'status is 200': (status) => status === 200 });
  check(response.content, { 'content is Agendamento iniciado com sucesso': (content) => content === 'Agendamento iniciado com sucesso' });
}

// Teste: Definir especialidade
export function test_set_specialty() {
  const payload = {
    "contact": {
      "name": "",
      "urn": "tel:+12065551212",
      "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
    },
    "flow": {
      "name": "fluxo_registro",
      "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
    },
    "results": {
      "message": {
        "category": "specialty",
        "value": "Clínico"
      }
    }
  };
  const response = make_post_request(`${host}/set_specialty`, payload);
  check(response.status, { 'status is 200': (status) => status === 200 });
  check(response.content, { 'content is Especialidade definida com sucesso': (content) => content === 'Especialidade definida com sucesso' });
}

// Teste: Definir unidade
export function test_set_unity() {
  const payload = {
    "contact": {
      "name": "",
      "urn": "tel:+12065551212",
      "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
    },
    "flow": {
      "name": "fluxo_registro",
      "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
    },
    "results": {
      "message": {
        "category": "message",
        "value": "1"
      }
    }
  };
  const response = make_post_request(`${host}/set_unity_consult`, payload);
  check(response.status, { 'status is 200': (status) => status === 200 });
  check(response.content, { 'content is Unidade definida com sucesso': (content) => content === 'Unidade definida com sucesso' });
}

// Teste: Definir data da consulta
export function test_set_consult_date() {
  const payload = {
    "contact": {
      "name": "",
      "urn": "tel:+12065551212",
      "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
    },
    "flow": {
      "name": "fluxo_registro",
      "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
    },
    "results": {
      "message": {
        "category": "date_schedule",
        "value": generate_random_date()
      }
    }
  };
  const response = make_post_request(`${host}/set_consult_date`, payload);
  check(response.status, { 'status is 200': (status) => status === 200 });
  check(response.content, { 'content is Data da consulta definida com sucesso': (content) => content === 'Data da consulta definida com sucesso' });
}

// Teste: Definir hora da consulta
export function test_set_consult_time() {
  const payload = {
    "contact": {
      "name": "",
      "urn": "tel:+12065551212",
      "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
    },
    "flow": {
      "name": "fluxo_registro",
      "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
    },
    "results": {
      "message": {
        "category": "time_schedule",
        "value": generate_random_time()
      }
    }
  };
  const response = make_post_request(`${host}/set_consult_time`, payload);
  check(response.status, { 'status is 200': (status) => status === 200 });
  check(response.content, { 'content is Hora da consulta definida com sucesso': (content) => content === 'Hora da consulta definida com sucesso' });
}

// Teste: Definir necessidade
export function test_set_necessity() {
  const payload = {
    "contact": {
      "name": "",
      "urn": "tel:+12065551212",
      "uuid": "a998eda6-caaa-47d1-9ffc-3fd7a9753c84"
    },
    "flow": {
      "name": "fluxo_registro",
      "uuid": "5b767bce-e0e8-4211-919f-4dd6e3c46913"
    },
    "results": {
      "message": {
        "category": "necessity",
        "value": "Finalizar"
      }
    }
  };
  const response = make_post_request(`${host}/set_necessity`, payload);
  check(response.status, { 'status is 200': (status) => status === 200 });
}

export default function () {
    test_register_consult();
    test_set_specialty();
    test_set_unity();
    test_set_consult_date();
    test_set_consult_time();
    test_set_necessity();
  }
